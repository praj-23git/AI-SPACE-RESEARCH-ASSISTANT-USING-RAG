from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load the mission document
loader = TextLoader("data/chandrayaan_3.txt")
documents = loader.load()

print("Document loaded successfully!")
print("Number of documents:", len(documents))

# Split the document into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print("Number of chunks:", len(chunks))

# Display each chunk
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk.page_content)