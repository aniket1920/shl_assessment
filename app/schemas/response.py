from pydantic import BaseModel

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