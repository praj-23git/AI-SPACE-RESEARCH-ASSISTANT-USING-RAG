from research_search import search_research_papers
from paper_loader import get_paper_text


papers = search_research_papers(
    "Mars biosignatures",
    limit=5
)


print("\n===================================")
print("       FULL TEXT PAPER TEST")
print("===================================\n")


for i, paper in enumerate(
    papers,
    start=1
):

    print(
        f"\n{i}. {paper['title']}"
    )

    print(
        "Open Access:",
        paper["is_open_access"]
    )

    print(
        "PDF:",
        paper["pdf_url"]
    )


    text = get_paper_text(
        paper
    )


    if text:

        print(
            "\nExtracted text:"
        )

        print(
            text[:1000]
        )

        print(
            "\nText length:",
            len(text),
            "characters"
        )

    else:

        print(
            "\nNo text available."
        )


    print(
        "\n-----------------------------------"
    )