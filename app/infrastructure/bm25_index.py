from rank_bm25 import BM25Okapi


class BM25Index:

    def __init__(self, documents):

        tokenized = [doc.split() for doc in documents]

        self.bm25 = BM25Okapi(tokenized)

    def search(self, query, k=20):

        scores = self.bm25.get_scores(query.split())

        top = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:k]

        return top
