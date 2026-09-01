from flask import Flask, render_template, request, jsonify

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM

from research_search import (
    search_research_papers,
    retrieve_research_passages
)


app = Flask(__name__)


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# LOAD EXISTING FAISS DATABASE
# =========================================================

vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


# =========================================================
# LOAD GEMMA
# =========================================================

llm = OllamaLLM(
    model="gemma2:2b"
)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# ASK
# =========================================================

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json() or {}

    question = data.get(
        "question",
        ""
    ).strip()

    history = data.get(
        "history",
        []
    )


    # =====================================================
    # EMPTY QUESTION
    # =====================================================

    if not question:

        return jsonify({

            "answer":
                "Please enter a question.",

            "sources": [],

            "evidence": [],

            "research_papers": []

        })


    # =====================================================
    # LOCAL KNOWLEDGE BASE RETRIEVAL
    # =====================================================

    results = vector_store.max_marginal_relevance_search(

        question,

        k=5,

        fetch_k=15,

        lambda_mult=0.7

    )


    # =====================================================
    # DEDUPLICATE LOCAL SOURCES
    # =====================================================

    unique_results = []

    seen_sources = set()


    for result in results:

        source = result.metadata.get(
            "source",
            result.metadata.get(
                "filename",
                "Unknown"
            )
        )

        filename = result.metadata.get(
            "filename",
            source
        )


        # Use filename as the primary identifier
        source_id = filename.lower().strip()


        if source_id in seen_sources:

            continue


        seen_sources.add(
            source_id
        )


        unique_results.append(
            result
        )


    # =====================================================
    # BUILD LOCAL KNOWLEDGE CONTEXT
    # =====================================================

    context_parts = []


    for i, result in enumerate(

        unique_results,

        start=1

    ):

        source = result.metadata.get(
            "source",
            "Unknown"
        )

        filename = result.metadata.get(
            "filename",
            source
        )

        category = result.metadata.get(
            "category",
            "Unknown"
        )

        context_parts.append(

            f"""
===== KNOWLEDGE BASE SOURCE {i} =====

FILE:
{filename}

CATEGORY:
{category}

CONTENT:
{result.page_content}

===== END KNOWLEDGE BASE SOURCE {i} =====
"""

        )


    # =====================================================
    # OPENALEX RESEARCH SEARCH
    # =====================================================

    research_papers = search_research_papers(

        question,

        limit=5

    )


    # =====================================================
    # RETRIEVE RESEARCH PASSAGES
    # =====================================================

    research_results = retrieve_research_passages(

        question,

        research_papers,

        k=5

    )


    # =====================================================
    # BUILD RESEARCH CONTEXT
    # =====================================================

    research_context_parts = []


    for i, result in enumerate(

        research_results,

        start=1

    ):

        research_context_parts.append(

            f"""
===== RESEARCH EVIDENCE {i} =====

TITLE:
{result.metadata.get('title', 'Unknown')}

AUTHORS:
{result.metadata.get('authors', 'Unknown')}

YEAR:
{result.metadata.get('year', 'Unknown')}

CONTENT:
{result.page_content}

PAPER URL:
{result.metadata.get('url', 'Not available')}

PDF URL:
{result.metadata.get('pdf_url', 'Not available')}

===== END RESEARCH EVIDENCE {i} =====
"""

        )


    research_context = "\n".join(
        research_context_parts
    )


    # =====================================================
    # CONVERSATION HISTORY
    # =====================================================

    previous_conversation = ""


    for message in history:

        role = message.get(
            "role",
            ""
        )

        content = message.get(
            "content",
            ""
        )

        previous_conversation += (

            f"{role}: {content}\n"

        )


    # =====================================================
    # RAG PROMPT
    # =====================================================

    prompt = f"""
You are a Space Mission Intelligence and Research Assistant.

Your job is to answer questions using the retrieved
knowledge base and research evidence.

You MUST ground your answer in the provided evidence.

IMPORTANT RULES:

1. Do not invent facts.

2. Do not use outside knowledge.

3. Keep facts associated with the correct entity.

4. Never mix information between different missions,
   companies, agencies, spacecraft, rockets, or organizations.

5. If research evidence is relevant, use it.

6. If multiple research papers are relevant, synthesize
   their information carefully.

7. Do not claim that a research paper says something
   unless that information appears in the retrieved
   research evidence.

8. For simple factual questions, answer directly.

9. For research questions, provide a concise synthesis
   based on the retrieved research evidence.

10. If the evidence does not contain enough information,
    say exactly:

"I don't have enough information in my knowledge base."


=========================================================
PREVIOUS CONVERSATION
=========================================================

{previous_conversation}


=========================================================
LOCAL KNOWLEDGE BASE
=========================================================

{chr(10).join(context_parts)}


=========================================================
ONLINE RESEARCH EVIDENCE
=========================================================

{research_context}


=========================================================
USER QUESTION
=========================================================

{question}


=========================================================
ANSWER
=========================================================
"""


    # =====================================================
    # GENERATE ANSWER
    # =====================================================

    answer = llm.invoke(
        prompt
    ).strip()


    # =====================================================
    # LOCAL SOURCES
    # =====================================================

    sources = []

    evidence = []


    for result in unique_results:

        source = result.metadata.get(
            "source",
            result.metadata.get(
                "filename",
                "Unknown"
            )
        )

        if source not in sources:

            sources.append(
                source
            )


        evidence.append({

            "source":
                source,

            "content":
                result.page_content

        })


    # =====================================================
    # RESEARCH PAPER METADATA
    # =====================================================

    research_paper_list = []


    seen_papers = set()


    for paper in research_papers:

        title = paper.get(
            "title",
            "Unknown"
        )


        if title in seen_papers:

            continue


        seen_papers.add(
            title
        )


        research_paper_list.append({

            "title":
                title,

            "authors":
                paper.get(
                    "authors",
                    []
                ),

            "year":
                paper.get(
                    "year",
                    "Unknown"
                ),

            "url":
                paper.get(
                    "url"
                ),

            "pdf_url":
                paper.get(
                    "pdf_url"
                ),

            "citation_count":
                paper.get(
                    "citation_count",
                    0
                ),

            "is_open_access":
                paper.get(
                    "is_open_access",
                    False
                )

        })


    # =====================================================
    # RETURN RESPONSE
    # =====================================================

    return jsonify({

        "answer":
            answer,

        "sources":
            sources,

        "evidence":
            evidence,

        "research_papers":
            research_paper_list

    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )