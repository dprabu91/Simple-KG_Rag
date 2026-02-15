# 🧠 Simple Knowledge Graph RAG with Neo4j

Load a FAQ file → Extract entities & relations → Store in Neo4j → Ask questions with AI

---

## 🔄 How It Works

FAQ.txt → LLM extracts entities & relations → Stored in Neo4j → Ask questions → AI answers!


---

## ⚡ Quick Setup (5 Minutes)

### 1️⃣ Create Neo4j Database (Free)

1. Go to https://neo4j.com/cloud/aura-free  
2. Sign up → Create **AuraDB Free** instance  
3. Save:
   - URI  
   - Username  
   - Password  

---

### 2️⃣ Create Project

```bash
mkdir kg-rag && cd kg-rag
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install openai neo4j python-dotenv numpy

4️⃣ Create .env File

OPENAI_API_KEY=sk-your-key-here
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password

5️⃣ Add FAQ Data
Create a file named faq.txt:

Q: What is AI?
A: Artificial Intelligence is a branch of computer science created by Alan Turing in 1950. Major labs include OpenAI, Google DeepMind, and Anthropic.

Q: What is Machine Learning?
A: Machine Learning is a subset of AI that learns from data. Popular frameworks include TensorFlow by Google and PyTorch by Meta.

Q: What is Deep Learning?
A: Deep Learning is a subset of Machine Learning using neural networks. Pioneers include Geoffrey Hinton and Yann LeCun. It powers image recognition and language models.

Q: What is NLP?
A: Natural Language Processing is a field of AI for human-computer language interaction. Key models include BERT by Google and GPT by OpenAI.

Q: What is a Knowledge Graph?
A: A Knowledge Graph stores entities and their relationships. Google introduced it in 2012. Neo4j is the most popular graph database for building them.

6️⃣ Run the Application
python app.py

💬 Example Usage
❓ Question: What is Machine Learning?

💡 Machine Learning is a subset of Artificial Intelligence that learns patterns from data.

🖼️ See Your Graph

Open Neo4j Browser and run:

MATCH (n)-[r]->(m) RETURN n, r, m
You'll see something like:

(AI) ←──SUBSET_OF── (Machine Learning) ←──SUBSET_OF── (Deep Learning)
 │                          │
 CREATED_BY              USED_IN
 │                          │
 ▼                          ▼
(Alan Turing)           (TensorFlow)──CREATED_BY──▶(Google)

🧩 How Each Step Works
Step	What It Does	One-Line Explanation
Load	Read faq.txt	Split FAQ into chunks by Q&A pairs
Extract	LLM reads each chunk	Returns entities (nouns) + relations (connections)
Store	Push to Neo4j	Creates nodes + edges in the graph database
Query	User asks question	Find matching graph nodes → send context to LLM → get answer

What is RAG?
Without RAG:  Question → LLM → Answer (guesses from training data)
With RAG:     Question → Search Database → LLM + Context → Accurate Answer ✅

🛠️ Troubleshooting
Problem	Fix
Connection refused	Check Neo4j is running + correct URI in .env
AuthError	Double-check Neo4j password in .env
openai.AuthenticationError	Check your OpenAI API key
Empty results	Make sure you ran the build phase first
🚀

🏗 Architecture
User Question
   │
   ├── Neo4j Knowledge Graph (Facts & Relations)
   ├── Vector Search (Semantic Similarity)
   │
   └── LLM Answer Synthesis

🚀 Features
✅ Knowledge Graph RAG

✅ Neo4j entity relationships

✅ Hybrid Graph + Vector RAG

✅ Hallucination-resistant answers

✅ Simple & extensible design


🧠 Tech Stack
OpenAI GPT

Neo4j AuraDB

Python

Vector Embeddings

Hybrid RAG

📌 Future Improvements
🔹 Neo4j Vector Index

🔹 FAISS integration

🔹 API / Streamlit UI

🔹 Answer confidence scoring

🔹 RAG evaluation metrics

⭐ If You Like This Project
Give it a ⭐ on GitHub and feel free to fork & improve!


---

## 3️⃣ Why This Looks Like Your Screenshot

| Feature | How |
|------|----|
Big title with emoji | `# 🧠 Title` |
Divider lines | `---` |
Code blocks | ``` |
Clickable links | Plain URLs |
Sections | `## Heading` |
Icons | Emojis (🚀 ⚡ 🧠) |

GitHub **automatically renders** everything — no CSS needed.

---

## 4️⃣ Optional: Make It Even Better 🔥

If you want, I can:
- Add **badges** (stars, license, python version)
- Add **architecture diagram (Mermaid)**
- Write **enterprise-level README**
- Optimize for **GitHub stars & SEO**
- Align it perfectly with **Hybrid RAG branding**

Just say **“enhance README”** and I’ll do it 🚀
