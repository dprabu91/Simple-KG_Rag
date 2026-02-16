# Knowledge Graph RAG Application

A Python-based application that extracts knowledge from FAQ documents, builds a knowledge graph using Neo4j, and enables intelligent retrieval-augmented generation (RAG) queries using OpenAI's language models.

## Overview

This project demonstrates a modern approach to knowledge management by:
1. **Extracting** entities and relationships from FAQ documents using LLM
2. **Storing** the knowledge graph in Neo4j for efficient querying
3. **Retrieving** relevant context from the graph
4. **Generating** intelligent responses using OpenAI's GPT models

## Features

- **Document Processing**: Loads and chunks FAQ documents
- **Entity & Relation Extraction**: Uses LLM (GPT-4) to automatically extract structured knowledge
- **Knowledge Graph Storage**: Stores extracted entities and relationships in Neo4j
- **Smart Retrieval**: Queries the knowledge graph to find relevant context
- **RAG Integration**: Combines retrieved knowledge with LLM for enhanced Q&A

## Project Structure

```
.
├── app.py                 # Main application code
├── faq.txt               # FAQ document source
├── vector_store.json     # Embeddings storage
├── .env                  # Environment variables (create this)
└── README.md            # This file
```

## Prerequisites

- Python 3.8+
- Neo4j Database (local or cloud instance)
- OpenAI API key

## Installation

1. **Clone or setup the project**
   ```bash
   cd KG_RAG_Nodej
   ```

2. **Install dependencies**
   ```bash
   pip install openai neo4j python-dotenv
   ```

3. **Create `.env` file** with your credentials:
   ```
   OPENAI_API_KEY=your_openai_api_key
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_neo4j_password
   ```

## Usage

Run the application:
```bash
python app.py
```

### How it Works

**Step 1: Load FAQ Document**
- Reads `faq.txt` and splits it into Q&A pairs
- Each pair becomes a chunk for processing

**Step 2: Extract Knowledge**
- Uses GPT-4o-mini to extract entities (concepts, technologies, people)
- Identifies relationships between entities (SUBSET_OF, CREATED_BY, etc.)
- Returns structured JSON with entities and relations

**Step 3: Store in Neo4j**
- Clears existing data
- Creates nodes for each entity
- Creates relationships to connect entities
- Enables graph traversal and pattern matching

**Step 4: Retrieve & Generate**
- Queries the graph for relevant entities and relationships
- Constructs context from retrieved knowledge
- Generates answers using the LLM with enhanced context

## Key Components

### `load_faq(path)`
Loads and chunks FAQ documents from a text file.

### `extract(chunk)`
Extracts entities and relationships from text using LLM.
- **Input**: Text chunk
- **Output**: JSON with entities and relations

### `store(entities, relations)`
Stores extracted knowledge in Neo4j.
- Creates entity nodes with properties
- Creates relationship edges between entities

### `retrieve(query)`
Searches the knowledge graph for relevant information.

### `generate(query)`
Generates answers using retrieved context from the knowledge graph.

## Data Sample

The application comes with a sample FAQ covering:
- Artificial Intelligence
- Machine Learning
- Deep Learning
- Natural Language Processing (NLP)
- Knowledge Graphs

Topics include key researchers, frameworks, and companies in AI/ML.

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | sk-... |
| `NEO4J_URI` | Neo4j database URI | bolt://localhost:7687 |
| `NEO4J_USERNAME` | Neo4j username | neo4j |
| `NEO4J_PASSWORD` | Neo4j password | your_password |

### LLM Settings

- **Model**: gpt-4o-mini
- **Temperature**: 0 (deterministic extraction)
- **Max tokens**: Default

## Example Query Flow

```
User: "Tell me about Machine Learning"
    ↓
[Retrieve relevant entities and relationships from Neo4j]
    ↓
[LLM generates answer using retrieved context]
    ↓
Response: "Machine Learning is a subset of AI..."
```

## Knowledge Graph Schema

### Entities
- **CONCEPT**: AI, Machine Learning, Deep Learning, NLP
- **PERSON**: Alan Turing, Geoffrey Hinton, Yann LeCun
- **ORGANIZATION**: OpenAI, Google DeepMind, Google, Meta
- **TECHNOLOGY**: TensorFlow, PyTorch, BERT, GPT
- **DATE**: 1950, 2012

### Relations
- `SUBSET_OF`: X is a subset of Y
- `CREATED_BY`: Created by a person/organization
- `USES`: System X uses technology Y
- `DEVELOPED_BY`: Framework developed by organization
- `INTRODUCED_IN`: Concept introduced in year Y

## Troubleshooting

### Neo4j Connection Issues
- Verify Neo4j is running
- Check connection URI and credentials
- Ensure firewall allows port 7687

### OpenAI API Errors
- Verify API key is correct
- Check API quota and billing
- Ensure model exists (gpt-4o-mini)

### Extraction Failures
- Review input text format
- Check for malformed JSON in LLM responses
- Verify LLM is returning valid JSON

## License

MIT License

## Contributors

Created as a demonstration of Knowledge Graph + RAG patterns.

## Resources

- [Neo4j Documentation](https://neo4j.com/docs/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [RAG Concepts](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
