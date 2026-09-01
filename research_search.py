import requests
import os
from dotenv import load_dotenv

load_dotenv()
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from paper_loader import get_paper_text


# =========================================================
# OPENALEX
# =========================================================

OPENALEX_URL = "https://api.openalex.org/works"

OPENALEX_API_KEY = os.getenv("OPENALEX_API_KEY")


# =========================================================
# EMBEDDING MODEL
# =========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# SEARCH OPENALEX
# =========================================================

def search_research_papers(query, limit=5):

    print("\n===================================")
    print("SEARCHING OPENALEX")
    print("QUERY:", query)
    print("===================================")

    query = str(query).strip()

    # OpenAlex exact search
    params = {
    "search.exact": query,
    "per-page": int(limit),
    "api_key": OPENALEX_API_KEY
}

    try:

        response = requests.get(
            OPENALEX_URL,
            params=params,
            timeout=30,
            headers={
                "User-Agent":
                    "Space-Mission-Research-Assistant/1.0"
            }
        )

        print(
            "REQUEST URL:",
            response.url
        )

        print(
            "STATUS:",
            response.status_code
        )

        if response.status_code != 200:

            print(
                "OPENALEX RESPONSE:",
                response.text[:1000]
            )

            return []

        data = response.json()

        results = data.get(
            "results",
            []
        )

        print(
            "OPENALEX RESULTS:",
            len(results)
        )

        papers = []

        for work in results:

            # -----------------------------------------
            # PAPER ID
            # -----------------------------------------

            paper_id = work.get(
                "id",
                ""
            )

            # -----------------------------------------
            # TITLE
            # -----------------------------------------

            title = work.get(
                "display_name",
                "Unknown title"
            )

            # -----------------------------------------
            # YEAR
            # -----------------------------------------

            year = work.get(
                "publication_year",
                "Unknown"
            )

            # -----------------------------------------
            # AUTHORS
            # -----------------------------------------

            authors = []

            for authorship in work.get(
                "authorships",
                []
            ):

                author = authorship.get(
                    "author",
                    {}
                )

                name = author.get(
                    "display_name"
                )

                if name:
                    authors.append(name)

            # -----------------------------------------
            # ABSTRACT
            # -----------------------------------------

            abstract = ""

            abstract_index = work.get(
                "abstract_inverted_index"
            )

            if abstract_index:

                words = []

                for word, positions in abstract_index.items():

                    for position in positions:

                        words.append(
                            (
                                position,
                                word
                            )
                        )

                words.sort(
                    key=lambda item: item[0]
                )

                abstract = " ".join(
                    word
                    for _, word in words
                )

            # -----------------------------------------
            # DOI
            # -----------------------------------------

            doi = work.get(
                "doi"
            )

            # -----------------------------------------
            # PRIMARY LOCATION
            # -----------------------------------------

            primary_location = (
                work.get(
                    "primary_location"
                )
                or {}
            )

            paper_url = primary_location.get(
                "landing_page_url"
            )

            pdf_url = primary_location.get(
                "pdf_url"
            )

            # -----------------------------------------
            # SEARCH OTHER LOCATIONS FOR PDF
            # -----------------------------------------

            if not pdf_url:

                for location in work.get(
                    "locations",
                    []
                ):

                    if not location:
                        continue

                    possible_pdf = location.get(
                        "pdf_url"
                    )

                    if possible_pdf:

                        pdf_url = possible_pdf

                        break

            # -----------------------------------------
            # FALLBACK URL
            # -----------------------------------------

            if not paper_url:

                paper_url = doi

            # -----------------------------------------
            # CITATIONS
            # -----------------------------------------

            citation_count = work.get(
                "cited_by_count",
                0
            )

            # -----------------------------------------
            # OPEN ACCESS
            # -----------------------------------------

            open_access = (
                work.get(
                    "open_access"
                )
                or {}
            )

            is_open_access = open_access.get(
                "is_oa",
                False
            )

            # -----------------------------------------
            # CREATE PAPER
            # -----------------------------------------

            paper = {

                "paper_id":
                    paper_id,

                "title":
                    title,

                "authors":
                    authors,

                "year":
                    year,

                "abstract":
                    abstract,

                "doi":
                    doi,

                "url":
                    paper_url,

                "pdf_url":
                    pdf_url,

                "citation_count":
                    citation_count,

                "is_open_access":
                    is_open_access

            }

            papers.append(
                paper
            )

            print(
                "FOUND:",
                title
            )

        print(
            "===================================\n"
        )

        return papers

    except requests.exceptions.RequestException as error:

        print(
            "OPENALEX REQUEST ERROR:",
            error
        )

        return []

    except Exception as error:

        print(
            "OPENALEX ERROR:",
            error
        )

        return []


# =========================================================
# CREATE RESEARCH DOCUMENTS
# =========================================================

def create_research_documents(papers):

    documents = []

    for paper in papers:

        title = paper.get(
            "title",
            "Unknown"
        )

        print(
            "\nExtracting:",
            title
        )

        # -----------------------------------------
        # TRY FULL TEXT
        # -----------------------------------------

        try:

            paper_text = get_paper_text(
                paper
            )

        except Exception as error:

            print(
                "Full text extraction failed:",
                error
            )

            paper_text = ""

        # -----------------------------------------
        # FALLBACK TO ABSTRACT
        # -----------------------------------------

        if not paper_text:

            paper_text = paper.get(
                "abstract",
                ""
            )

        if not paper_text:

            print(
                "No text available:",
                title
            )

            continue

        authors = ", ".join(
            paper.get(
                "authors",
                []
            )
        )

        # -----------------------------------------
        # DOCUMENT CONTENT
        # -----------------------------------------

        content = f"""
TITLE:
{title}

AUTHORS:
{authors}

YEAR:
{paper.get('year', 'Unknown')}

RESEARCH CONTENT:
{paper_text}
"""

        document = Document(

            page_content=content,

            metadata={

                "type":
                    "research_paper",

                "paper_id":
                    paper.get(
                        "paper_id",
                        ""
                    ),

                "title":
                    title,

                "authors":
                    authors,

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
                    )

            }

        )

        documents.append(
            document
        )

    print(
        "\nRESEARCH DOCUMENTS:",
        len(documents)
    )

    return documents


# =========================================================
# SPLIT RESEARCH DOCUMENTS
# =========================================================

def split_research_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=150

    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        "RESEARCH CHUNKS:",
        len(chunks)
    )

    return chunks


# =========================================================
# RETRIEVE RESEARCH PASSAGES
# =========================================================

def retrieve_research_passages(
    question,
    papers,
    k=5
):

    if not papers:

        print(
            "No OpenAlex papers available."
        )

        return []

    documents = create_research_documents(
        papers
    )

    if not documents:

        print(
            "No research documents created."
        )

        return []

    chunks = split_research_documents(
        documents
    )

    if not chunks:

        return []

    print(
        "\nCreating temporary research FAISS index..."
    )

    research_vector_store = FAISS.from_documents(

        chunks,

        embeddings

    )

    candidate_count = min(

        max(k * 3, 10),

        len(chunks)

    )

    results = research_vector_store.similarity_search(

        question,

        k=candidate_count

    )

    # -----------------------------------------
    # REMOVE DUPLICATE PAPERS
    # -----------------------------------------

    final_results = []

    seen_papers = set()

    for result in results:

        paper_id = result.metadata.get(
            "paper_id"
        )

        title = result.metadata.get(
            "title",
            "Unknown"
        )

        identifier = (
            paper_id
            or
            title
        )

        if identifier in seen_papers:

            continue

        seen_papers.add(
            identifier
        )

        final_results.append(
            result
        )

        if len(final_results) >= k:

            break

    print(
        "\nFINAL RESEARCH RESULTS:",
        len(final_results)
    )

    for result in final_results:

        print(
            "-",
            result.metadata.get(
                "title",
                "Unknown"
            )
        )

    print()

    return final_results