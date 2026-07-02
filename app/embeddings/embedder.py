from sentence_transformers import SentenceTransformer

class CatalogEmbedder:

    def __init__(
        self,
        model_name="BAAI/bge-small-en-v1.5"
    ):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )