from app.infrastructure.dataset_loader import load_documents
from app.infrastructure.bm25_index import BM25Index
from app.infrastructure.vector_store import VectorStore
from app.infrastructure.reranker import Reranker
from app.infrastructure.gemini_llm import GeminiLLM
from app.utils.text_utils import normalize


class RAGService:

    def __init__(self):

        self.raw_docs, self.documents = load_documents()

        self.bm25 = BM25Index(self.documents)

        self.vector = VectorStore(self.raw_docs)

        self.reranker = Reranker()

        self.llm = GeminiLLM()

    def hybrid_retrieve(self, query):

        q = normalize(query)

        bm25_indices = self.bm25.search(q)

        bm25_docs = [self.raw_docs[i] for i in bm25_indices]

        dense_docs = self.vector.search(query)

        candidates = list(set(bm25_docs + dense_docs))

        return self.reranker.rerank(query, candidates)

    def ask(self, query):

        docs = self.hybrid_retrieve(query)

        context = "\n\n".join(docs)

        prompt = f"""
Anda adalah asisten regulasi pendidikan tinggi Indonesia.

SELURUH jawaban WAJIB menggunakan Bahasa Indonesia formal.

Jawablah hanya berdasarkan konteks berikut.

Konteks:
{context}

Pertanyaan:
{query}

Jawaban:
"""

        return self.llm.generate(prompt)
