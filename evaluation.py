from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM

from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from bert_score import score


# -----------------------------
# Load RAG
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

llm = OllamaLLM(model="gemma2:2b")


# -----------------------------
# Evaluation dataset
# -----------------------------

evaluation_data = [
    {
        "question": "What is Hayabusa2?",
        "expected": "Hayabusa2 was a JAXA mission to explore asteroid Ryugu and return samples to Earth."
    },
    {
        "question": "Who operated Chandrayaan-3?",
        "expected": "Chandrayaan-3 was operated by the Indian Space Research Organisation ISRO."
    },
    {
        "question": "What is the destination of Hayabusa2?",
        "expected": "Hayabusa2's destination was asteroid Ryugu."
    },
    {
        "question": "What is SpaceX's Falcon 9?",
        "expected": "Falcon 9 is a reusable rocket developed by SpaceX."
    },
    {
        "question": "What is Vikram-S?",
        "expected": "Vikram-S is a rocket developed by Skyroot Aerospace."
    }
]


# -----------------------------
# Metric setup
# -----------------------------

rouge = rouge_scorer.RougeScorer(
    ["rouge1", "rougeL"],
    use_stemmer=True
)

smooth = SmoothingFunction().method1


rouge_scores = []
bleu_scores = []
bert_scores = []


print("\nRAG EVALUATION\n")

for item in evaluation_data:

    question = item["question"]
    expected = item["expected"]

    results = vector_store.max_marginal_relevance_search(
        question,
        k=5,
        fetch_k=15,
        lambda_mult=0.7
    )

    context = "\n\n".join(
        r.page_content for r in results
    )

    prompt = f"""
You are a Space Mission Assistant.

Answer using ONLY the context.

Context:
{context}

Question:
{question}

Answer:
"""

    generated = llm.invoke(prompt).strip()

    # ROUGE
    rouge_result = rouge.score(expected, generated)

    rouge_l = rouge_result["rougeL"].fmeasure

    # BLEU
    bleu = sentence_bleu(
        [expected.split()],
        generated.split(),
        smoothing_function=smooth
    )

    # BERTScore
    _, _, f1 = score(
        [generated],
        [expected],
        lang="en",
        verbose=False
    )

    bert = float(f1[0])

    rouge_scores.append(rouge_l)
    bleu_scores.append(bleu)
    bert_scores.append(bert)

    print("=" * 60)
    print("Question :", question)
    print("Expected :", expected)
    print("Generated:", generated)
    print(f"ROUGE-L : {rouge_l:.3f}")
    print(f"BLEU    : {bleu:.3f}")
    print(f"BERT    : {bert:.3f}")
    print()

print("=" * 60)
print("AVERAGE SCORES")
print(f"ROUGE-L : {sum(rouge_scores)/len(rouge_scores):.3f}")
print(f"BLEU    : {sum(bleu_scores)/len(bleu_scores):.3f}")
print(f"BERT    : {sum(bert_scores)/len(bert_scores):.3f}")