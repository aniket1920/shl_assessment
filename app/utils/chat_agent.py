from app.conversation.prompts import build_context
from app.utils.helper import latest_user_message, is_vague

class ChatAgent:

    def __init__(self, retriever, embedder, llm):
        self.retriever = retriever
        self.embedder = embedder
        self.llm = llm

    def chat(self, conversation):
        context = build_context(conversation)
        query = latest_user_message(conversation)
        # Ask clarification if query is vague
        if is_vague(query):
            return {
                "reply": "Could you tell me the role, seniority level, or important skills you're hiring for?",
                "recommendations": []
            }
        # Encode query
        query_embedding = self.embedder.encode([query])
        # Retrieve assessments
        results = self.retriever.search(
            query=query,
            query_embedding=query_embedding,
            top_k=5
        )
        assessment_text = ""
        for result in results:
            assessment_text += f"""
Name: {result["name"]}
Assessment Type: {result["assessment_type"]}
Job Level: {result["job_level"]}
Duration: {result["duration"]}
URL: {result["url"]}

"""
        explanation = self.llm.recommend(
            query=context,
            assessments=assessment_text
        )
        return {
            "reply": explanation,
            "recommendations": results
        }