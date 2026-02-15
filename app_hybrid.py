import os
import json
import numpy as np
from openai import OpenAI
from neo4j import GraphDatabase
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# ENV + CLIENTS
# ─────────────────────────────────────────────
load_dotenv()

ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

db = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)

VECTOR_DB = "vector_store.json"

# ─────────────────────────────────────────────
# STEP 1: Load Document
# ─────────────────────────────────────────────
def load_faq(path="faq.txt"):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    print(f"📄 Loaded {len(chunks)} chunks")
    return chunks

# ─────────────────────────────────────────────
# STEP 2: Extract Entities & Relations (LLM)
# ─────────────────────────────────────────────
def extract(chunk):
    prompt = f"""
Extract entities and relations from this text.
Return ONLY valid JSON like:
{{
  "entities": [{{"name": "AI", "type": "CONCEPT"}}],
  "relations": [{{"source": "ML", "relation": "SUBSET_OF", "target": "AI"}}]
}}

Text:
{chunk}
"""

    res = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text = res.choices[0].message.content.strip()

    if "```" in text:
        text = text.split("```")[1].removeprefix("json").strip()

    try:
        return json.loads(text)
    except:
        return {"entities": [], "relations": []}

# ─────────────────────────────────────────────
# STEP 3: Store in Neo4j
# ─────────────────────────────────────────────
def store(entities, relations):
    with db.session() as s:
        s.run("MATCH (n) DETACH DELETE n")

        for e in entities:
            s.run(
                "MERGE (n:Entity {name:$name}) SET n.type=$type",
                name=e["name"],
                type=e["type"]
            )

        for r in relations:
            s.run(
                """
                MATCH (a:Entity {name:$src}), (b:Entity {name:$tgt})
                MERGE (a)-[:RELATES {type:$rel}]->(b)
                """,
                src=r["source"],
                rel=r["relation"],
                tgt=r["target"]
            )

    print(f"💾 Stored {len(entities)} entities, {len(relations)} relations")

# ─────────────────────────────────────────────
# STEP 4: GRAPH SEARCH (EXISTING RAG)
# ─────────────────────────────────────────────
def search_graph(question):
    res = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f'Extract keywords from this question as JSON array: "{question}"'
        }],
        temperature=0
    )

    text = res.choices[0].message.content.strip()

    if "```" in text:
        text = text.split("```")[1].removeprefix("json").strip()

    keywords = json.loads(text)

    results = []

    with db.session() as s:
        for kw in keywords:
            records = s.run(
                """
                MATCH (n:Entity)
                WHERE toLower(n.name) CONTAINS toLower($kw)
                OPTIONAL MATCH (n)-[r:RELATES]->(m)
                OPTIONAL MATCH (p)-[r2:RELATES]->(n)
                RETURN n.name AS entity, n.type AS type,
                       collect(DISTINCT {rel:r.type, target:m.name}) AS out,
                       collect(DISTINCT {rel:r2.type, source:p.name}) AS inc
                """,
                kw=kw
            )

            for rec in records:
                d = rec.data()
                info = f"{d['entity']} ({d['type']})"

                for o in d["out"]:
                    if o["target"]:
                        info += f"\n  → {d['entity']} --{o['rel']}--> {o['target']}"

                for i in d["inc"]:
                    if i["source"]:
                        info += f"\n  ← {i['source']} --{i['rel']}--> {d['entity']}"

                results.append(info)

    return "\n\n".join(results) if results else "No graph info found."

# ─────────────────────────────────────────────
# STEP 5: EMBEDDINGS (VECTOR RAG)
# ─────────────────────────────────────────────
def embed(text):
    res = ai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return res.data[0].embedding

def build_vector_store(chunks):
    vectors = []
    for i, chunk in enumerate(chunks):
        vectors.append({
            "id": i,
            "text": chunk,
            "embedding": embed(chunk)
        })

    with open(VECTOR_DB, "w") as f:
        json.dump(vectors, f)

    print(f"📦 Vector store created with {len(vectors)} chunks")

def cosine_sim(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_vectors(question, top_k=3):
    with open(VECTOR_DB) as f:
        vectors = json.load(f)

    q_emb = embed(question)

    scored = []
    for v in vectors:
        score = cosine_sim(q_emb, v["embedding"])
        scored.append((score, v["text"]))

    scored.sort(reverse=True, key=lambda x: x[0])

    return "\n\n".join([s[1] for s in scored[:top_k]])

# ─────────────────────────────────────────────
# STEP 6: HYBRID CONTEXT
# ─────────────────────────────────────────────
def hybrid_context(question):
    graph_ctx = search_graph(question)
    vector_ctx = search_vectors(question)

    return f"""
=== Knowledge Graph Context ===
{graph_ctx}

=== Semantic FAQ Context ===
{vector_ctx}
"""

# ─────────────────────────────────────────────
# STEP 7: HYBRID ASK
# ─────────────────────────────────────────────
def ask_hybrid(question):
    context = hybrid_context(question)

    res = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer using both Knowledge Graph facts and "
                    "semantic FAQ context. Prefer graph facts if conflict exists."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        temperature=0.3
    )

    return res.choices[0].message.content

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":

    print("\n🚀 Building Knowledge Graph...\n")
    chunks = load_faq()

    all_entities, all_relations = [], []
    seen_e, seen_r = set(), set()

    for i, chunk in enumerate(chunks):
        print(f"🧠 Extracting chunk {i+1}/{len(chunks)}")
        data = extract(chunk)

        for e in data["entities"]:
            if e["name"] not in seen_e:
                seen_e.add(e["name"])
                all_entities.append(e)

        for r in data["relations"]:
            key = (r["source"], r["relation"], r["target"])
            if key not in seen_r:
                seen_r.add(key)
                all_relations.append(r)

    store(all_entities, all_relations)

    print("\n📦 Building Vector Store...\n")
    build_vector_store(chunks)

    print("\n💬 Hybrid RAG Ready (type 'quit' to exit)\n")

    while True:
        q = input("❓ Question: ").strip()
        if q.lower() in ["quit", "exit", "q"]:
            break
        if q:
            print(f"\n💡 {ask_hybrid(q)}\n")

    db.close()
