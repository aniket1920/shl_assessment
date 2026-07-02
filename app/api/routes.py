from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.agent.service import AgentService

import pandas as pd
import numpy as np
from app.retrieval.bm25 import BM25Retriever

from app.conversation.recommender import LLMRecommender
router = APIRouter()
# ----------------------------
# Load everything ONCE
# ----------------------------
df = pd.read_csv("data/processed/catalog_processed.csv")
retriever = BM25Retriever(df)
llm = LLMRecommender()
agent = AgentService(
    retriever,
    None,
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