from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load the same embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load our existing FAISS database
vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# Ask a question
query = "When did Chandrayaan-3 land on the Moon?"

# Search for the 3 most relevant chunks
results = vector_store.similarity_search(query, k=3)

# Display the results
print("\nSearch results:\n")

for i, result in enumerate(results):
    print(f"--- Result {i + 1} ---")
    print(result.page_content)
    print()