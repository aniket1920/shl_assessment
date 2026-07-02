import ollama

from app.schemas import response

class LLMRecommender:

    def __init__(self, model="llama3.2:3b"):
        self.model = model
    def recommend(self, query, assessments):
        prompt = f"""
You are an SHL assessment recommendation assistant.

Below is the conversation with the recruiter.

Conversation:
{query}

Recommended SHL assessments:
{assessments}

For each assessment:

- explain why it matches the hiring need
- mention the skills evaluated
- keep the explanation concise
- do not invent assessments
- only use the assessments provided
"""
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response["message"]["content"]
    
    def compare(self, question, assessments):

        prompt = f"""
You are an SHL consultant.

Question:

{question}

Products

{assessments}

Compare these products.

Explain:

- purpose
- what each measures
- when to choose each
- differences

Keep it concise.
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        return response["message"]["content"]