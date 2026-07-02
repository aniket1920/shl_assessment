from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    conversation: list | None = None