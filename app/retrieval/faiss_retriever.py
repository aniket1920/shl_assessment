import faiss
import numpy as np
import pandas as pd

class FaissRetriever:

    def __init__(self, df, embeddings):
        self.df = df
        self.embeddings = embeddings.astype("float32")
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(self.embeddings)

    def search(
        self,
        query_embedding,
        top_k=10,
    ):
        scores, indices = self.index.search(
            query_embedding.astype("float32"),
            top_k,
        )
        results = []
        for idx, score in zip(indices[0], scores[0]):
            row = self.df.iloc[int(idx)]
            results.append({
                "index": int(idx),
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