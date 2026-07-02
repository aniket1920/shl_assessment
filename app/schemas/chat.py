from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    conversation: list[Message]

class Recommendation(BaseModel):
    name: str
    url: str
    assessment_type: str
    job_level: str
    duration: str
    score: float

class ChatResponse(BaseModel):
    reply: str
    recommendations: list[Recommendation]