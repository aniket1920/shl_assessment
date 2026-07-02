from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.agent.service import AgentService
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.faiss_retriever import FaissRetriever
from app.retrieval.hybrid import HybridRetriever
from app.conversation.recommender import LLMRecommender
router = APIRouter()
# ----------------------------
# Load everything ONCE
# ----------------------------
df = pd.read_csv("data/processed/catalog_processed.csv")
embeddings = np.load("data/embeddings/catalog_embeddings.npy")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
bm25 = BM25Retriever(df)
faiss = FaissRetriever(df, embeddings)
retriever = HybridRetriever(
    bm25=bm25,
    faiss=faiss
)
llm = LLMRecommender()
agent = AgentService(
    retriever,
    embedder,
    llm
)
# ----------------------------
# Health
# ----------------------------
@router.get("/")
def health():
    return {
        "status": "running",
        "message": "SHL Assessment Recommendation API"
    }
# ----------------------------
# Chat Endpoint
# ----------------------------
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    conversation = [
        {
            "role": message.role,
            "content": message.content
        }
        for message in request.conversation
    ]
    response = agent.chat(conversation)
    return response