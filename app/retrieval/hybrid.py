class HybridRetriever:

    def __init__(self, bm25, faiss):
        self.bm25 = bm25
        self.faiss = faiss

    def reciprocal_rank_fusion(
        self,
        bm25_results,
        faiss_results,
        k=60,
    ):

        fused = {}

        for rank, result in enumerate(bm25_results):
            idx = result["index"]

            if idx not in fused:
                fused[idx] = result.copy()

            fused[idx]["score"] = fused[idx].get(
                "score", 0
            ) + 1 / (k + rank + 1)

        for rank, result in enumerate(faiss_results):
            idx = result["index"]

            if idx not in fused:
                fused[idx] = result.copy()

            fused[idx]["score"] = fused[idx].get(
                "score", 0
            ) + 1 / (k + rank + 1)

        return sorted(
            fused.values(),
            key=lambda x: x["score"],
            reverse=True,
        )
    
    def search(
        self,
        query,
        query_embedding,
        top_k=10,
    ):
        bm25_results = self.bm25.search(query, top_k=20)
        faiss_results = self.faiss.search(query_embedding, top_k=20)
        fused = self.reciprocal_rank_fusion(
            bm25_results,
            faiss_results,
        )
        return fused[:top_k]