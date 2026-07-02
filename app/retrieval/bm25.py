from rank_bm25 import BM25Okapi
import pandas as pd

class BM25Retriever:
    """
    BM25-based keyword retriever for SHL assessments.
    """
    def __init__(self, df):
        self.df = df
        self.documents = df["search_document"].tolist()
        self.tokenized_docs = [
            doc.lower().split()
            for doc in self.documents
        ]
        self.bm25 = BM25Okapi(self.tokenized_docs)

    def search(self, query, top_k=10):
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )
        results = []
        for idx, score in ranked[:top_k]:
            row = self.df.iloc[idx]
            results.append({
                "index": idx,
                "score": float(score),
                "name": "" if pd.isna(row["name"]) else str(row["name"]),
                "url": "" if pd.isna(row["link"]) else str(row["link"]),
                "assessment_type": "" if pd.isna(row["assessment_type"]) else str(row["assessment_type"]),
                "job_level": "" if pd.isna(row["job_level"]) else str(row["job_level"]),
                "duration": (
                    "Unknown"
                    if pd.isna(row["duration"])
                    else str(row["duration"])
                ),  
            })
        return results