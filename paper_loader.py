import io
import requests

from pypdf import PdfReader


# =========================================================
# DOWNLOAD PDF
# =========================================================

def download_pdf(pdf_url):

    if not pdf_url:
        return None

    try:

        response = requests.get(
            pdf_url,
            timeout=30,
            headers={
                "User-Agent":
                    "Mozilla/5.0 "
                    "(compatible; "
                    "SpaceMissionResearchAssistant/1.0)"
            },
            allow_redirects=True
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if (
            "pdf" not in content_type
            and not response.content.startswith(b"%PDF")
        ):
            return None

        return response.content

    except requests.RequestException as error:

        print(
            f"PDF download failed: {error}"
        )

        return None


# =========================================================
# EXTRACT TEXT
# =========================================================

def extract_pdf_text(pdf_bytes):

    if not pdf_bytes:
        return ""

    try:

        pdf_file = io.BytesIO(
            pdf_bytes
        )

        reader = PdfReader(
            pdf_file
        )

        pages = []

        for page in reader.pages:

            try:

                text = page.extract_text()

                if text:
                    pages.append(text)

            except Exception:

                continue


        text = "\n\n".join(
            pages
        ).strip()


        return text


    except Exception as error:

        print(
            f"PDF extraction failed: {error}"
        )

        return ""


# =========================================================
# GET FULL TEXT
# =========================================================

def get_paper_text(paper):

    abstract = paper.get(
        "abstract",
        ""
    )


    # -----------------------------------------------------
    # Only try PDF when the paper is marked open access.
    # -----------------------------------------------------

    if not paper.get(
        "is_open_access",
        False
    ):

        return abstract


    pdf_url = paper.get(
        "pdf_url"
    )


    if not pdf_url:

        print(
            "No accessible PDF URL found."
        )

        return abstract


    # -----------------------------------------------------
    # Try downloading the PDF.
    # -----------------------------------------------------

    pdf_bytes = download_pdf(
        pdf_url
    )


    if not pdf_bytes:

        print(
            "Falling back to abstract."
        )

        return abstract


    # -----------------------------------------------------
    # Extract text.
    # -----------------------------------------------------

    text = extract_pdf_text(
        pdf_bytes
    )


    if not text:

        print(
            "No readable PDF text. "
            "Falling back to abstract."
        )

        return abstract


    # -----------------------------------------------------
    # Avoid returning extremely short extraction results.
    # -----------------------------------------------------

    if len(text) < 1000:

        print(
            "Extracted text is too short. "
            "Using abstract instead."
        )

        return abstract


    return text