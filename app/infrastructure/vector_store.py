from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import CHROMA_DB_DIR


class VectorStore:

    def __init__(self, raw_docs):

        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vectorstore = Chroma.from_texts(
            raw_docs,
            embedding=embedding,
            persist_directory=CHROMA_DB_DIR
        )

    def search(self, query, k=20):

        results = self.vectorstore.similarity_search(query, k=k)

        return [r.page_content for r in results]
