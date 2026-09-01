# 🚀 Space Mission Research Assistant

A Retrieval-Augmented Generation (RAG) based research assistant for exploring **space missions, spacecraft, space agencies, launch vehicles, and scientific research papers**.

The system combines a locally maintained space-mission knowledge base with **FAISS semantic search**, **OpenAlex research-paper retrieval**, and **Gemma 2B** to generate evidence-grounded answers.

---

## 📌 Overview

Finding reliable information about space missions often requires searching across mission documentation, agency information, technical resources, and scientific publications.

The **Space Mission Research Assistant** provides a single interface where users can ask questions about space exploration and receive answers based on:

- 📚 A local space-mission knowledge base
- 🔎 Semantic retrieval using FAISS
- 🔬 Scientific research papers retrieved from OpenAlex
- 🧠 Gemma 2B for answer generation
- 💬 Conversation history for contextual questions

Instead of relying entirely on the language model's internal knowledge, the system retrieves relevant information first and uses that evidence to generate the response.

---

## ✨ Features

### 📚 Knowledge Base RAG

Retrieves relevant information from a locally stored collection of space-related documents using semantic similarity search.

### 🔎 FAISS Vector Search

Documents are converted into vector embeddings using:

**`sentence-transformers/all-MiniLM-L6-v2`**

and stored in a FAISS vector database for efficient semantic retrieval.

### 🔬 Research Paper Search

For research-oriented questions, the system queries the **OpenAlex API** to discover relevant scientific publications.

Retrieved papers include information such as:

- Paper title
- Authors
- Publication year
- Citation count
- Open-access availability
- Paper URL
- PDF URL when available

### 📄 Research Evidence Retrieval

The system does not simply display paper titles.

Relevant passages are extracted from the retrieved research material and supplied to the RAG pipeline as research evidence.

### 🧠 Evidence-Grounded Generation

Gemma 2B generates answers using the retrieved knowledge-base information and research evidence.

The prompt instructs the model to:

- Avoid inventing facts
- Use retrieved evidence
- Keep information associated with the correct mission or organization
- Avoid mixing unrelated entities
- Clearly acknowledge when sufficient evidence is unavailable

### 💬 Conversation History

Previous questions and answers are passed to the assistant so that follow-up questions can be handled with conversational context.

### 🖥️ Interactive Web Interface

A space-themed Flask web interface provides:

- Question input
- Loading indicator
- Generated answers
- Knowledge-base evidence
- Research papers
- Paper links
- PDF links
- Clear conversation functionality

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       User           │
                    │   Space Question     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Flask App       │
                    │      /ask API        │
                    └──────────┬───────────┘
                               │
              ┌────────────────┴─────────────────┐
              │                                  │
              ▼                                  ▼
    ┌────────────────────┐             ┌────────────────────┐
    │ Local Knowledge    │             │     OpenAlex       │
    │ Base               │             │ Research Search    │
    └─────────┬──────────┘             └─────────┬──────────┘
              │                                  │
              ▼                                  ▼
    ┌────────────────────┐             ┌────────────────────┐
    │ Sentence           │             │ Research Papers    │
    │ Transformer        │             │ & Metadata         │
    │ Embeddings         │             └─────────┬──────────┘
    └─────────┬──────────┘                       │
              │                                  ▼
              ▼                         ┌────────────────────┐
    ┌────────────────────┐               │ Relevant Research │
    │      FAISS         │               │     Passages      │
    │   Vector Search    │               └─────────┬──────────┘
    └─────────┬──────────┘                         │
              │                                  │
              └────────────────┬─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │   Retrieved Evidence │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Gemma 2B        │
                    │    RAG Generation    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Research Answer    │
                    │   + Sources          │
                    │   + Research Papers  │
                    └──────────────────────┘
```

# 📸 Screenshots

### Main Interface

The SpaceRAG interface provides a simple space-themed interface for asking questions about missions, spacecraft, agencies, and scientific research.

<img width="929" height="374" alt="image" src="https://github.com/user-attachments/assets/088d57fd-6fd5-4930-8343-ff3b024fbd71" />


---

### RAG-Based Research Answer

The assistant retrieves relevant knowledge and generates an evidence-grounded response using Gemma 2B.

<img width="735" height="392" alt="image copy" src="https://github.com/user-attachments/assets/ea5b6ba5-3332-4463-8f9c-02102b166c44" />



---

### Research Papers

Research-oriented questions can retrieve relevant scientific papers through OpenAlex. The interface displays paper metadata along with links to the available paper or PDF.

<img width="886" height="500" alt="image copy 3" src="https://github.com/user-attachments/assets/a86cdb0c-cb92-4e11-8a28-05d05af69481" />

