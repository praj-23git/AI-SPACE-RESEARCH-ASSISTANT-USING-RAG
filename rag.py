from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM


# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load FAISS vector database
vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


# Load Gemma through Ollama
llm = OllamaLLM(model="gemma2:2b")


print("===================================")
print("     SPACE MISSION ASSISTANT")
print("===================================")
print("Ask questions about the available missions.")
print("Type 'exit' to stop.\n")


while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break


    # Retrieve relevant and diverse chunks
    results = vector_store.max_marginal_relevance_search(
        question,
        k=5,
        fetch_k=15,
        lambda_mult=0.7
    )


    # Combine retrieved information
    context = "\n\n".join(
        result.page_content for result in results
    )


    # Create prompt
    prompt = f"""
You are a Space Mission Assistant.

Answer the user's question using ONLY the information
provided in the context.

If the answer cannot be found in the context, say:
"I don't have enough information in my knowledge base."

Context:
{context}

Question:
{question}

Answer:
"""


    # Generate answer
    answer = llm.invoke(prompt)


    # Display answer
    print("\nAssistant:", answer)


    # Display sources
    print("\nSources:")

    sources = set()

    for result in results:
        source = result.metadata.get("source", "Unknown")
        sources.add(source)


    for source in sources:
        print(f"- {source}")

    print()