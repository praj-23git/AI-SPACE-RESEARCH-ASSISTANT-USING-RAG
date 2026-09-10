# 🚀 SpaceRAG: AI-Powered Space Mission Research Assistant

A Retrieval-Augmented Generation (RAG) based research assistant for exploring **space missions, spacecraft, space agencies, launch vehicles, and scientific research papers**.

The system combines a locally maintained space-mission knowledge base with **FAISS semantic search**, **OpenAlex research-paper retrieval**, and **Gemma 2B** to generate evidence-grounded answers.

---

## 📌 Overview

The Space Mission Research Assistant was developed to explore how Retrieval-Augmented Generation can be used to provide reliable, context-based answers about space exploration.

The project combines two information sources:

- 📚 A local space-mission knowledge base
- 🔬 Scientific research papers retrieved through OpenAlex

The system retrieves relevant information before generating an answer, allowing the language model to work with supporting evidence instead of relying only on its internal knowledge.

---

# 🛣️ Project Journey

The project was developed in **two main parts**.

## Part 1 — Building and Testing the Local RAG System

The first part focused on building and understanding the core RAG pipeline.

A space-mission dataset was created and used as the initial knowledge source. The documents were processed into vector embeddings using Sentence Transformers and stored in a FAISS vector database.

The RAG system was then tested with different questions to check whether it could:

- Retrieve relevant documents from the dataset
- Identify the correct information for a question
- Provide retrieved information as context to the language model
- Generate answers based on the retrieved context
- Keep information associated with the correct mission, agency, or spacecraft
- Avoid mixing information between different entities

### Initial RAG Pipeline

```text
Space Mission Dataset
        ↓
Document Processing
        ↓
Sentence Transformer Embeddings
        ↓
FAISS Vector Database
        ↓
Semantic Retrieval
        ↓
Retrieved Context
        ↓
Gemma 2B
        ↓
Generated Answer
```
## Part 2 — Connecting OpenAlex for Scientific Research

After successfully building and testing the local RAG system, the second part of the project focused on extending it with an external scientific research source.

I integrated the **OpenAlex API** to dynamically search for relevant scientific research papers based on the user's question. The system retrieves information such as:

- Paper title
- Authors
- Publication year
- Citation count
- Open-access availability
- Paper URL
- PDF URL when available

The retrieved research papers are then processed to find relevant research passages. These passages are provided to the RAG pipeline as additional evidence along with the information retrieved from the local knowledge base.

This allowed the system to answer research-oriented questions using both the **local space-mission knowledge base** and **scientific research literature**.

### Extended RAG Pipeline

```text
User Question
      ↓
Local Knowledge Base + OpenAlex Research Search
      ↓
FAISS Retrieval + Research Papers
      ↓
Relevant Research Evidence
      ↓
Gemma 2B
      ↓
Generated Answer
      ↓
Knowledge Base Evidence + Research Papers
```
## 🏗️ System Architecture

The system combines a local knowledge base, FAISS vector search, OpenAlex research retrieval, and Gemma 2B to generate evidence-grounded answers.

```text
                         ┌─────────────────────┐
                         │        User         │
                         │    Enters Question  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Flask App      │
                         │       /ask API      │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌──────────────────┐            ┌──────────────────┐
          │ Local Knowledge  │            │     OpenAlex     │
          │      Base        │            │  Research Search │
          └────────┬─────────┘            └────────┬─────────┘
                   │                               │
                   ▼                               ▼
          ┌──────────────────┐            ┌──────────────────┐
          │    Sentence      │            │ Research Papers  │
          │    Transformer   │            │    & Metadata    │
          │    Embeddings    │            └────────┬─────────┘
          └────────┬─────────┘                     │
                   │                               ▼
                   ▼                      ┌──────────────────┐
          ┌──────────────────┐            │    Research      │
          │      FAISS       │            │    Passages      │
          │ Semantic Search  │            │    Retrieval     │
          └────────┬─────────┘            └────────┬─────────┘
                   │                               │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │  Retrieved Evidence │
                        │ Local + Research    │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │      Gemma 2B       │
                        │   via Ollama        │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │   Generated Answer  │
                        └──────────┬──────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     │                           │
                     ▼                           ▼
          ┌────────────────────┐       ┌────────────────────┐
          │ Knowledge Base     │       │  Research Papers   │
          │ Evidence           │       │  & Paper Links     │
          └────────────────────┘       └────────────────────┘
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

