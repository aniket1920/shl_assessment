import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LLMRecommender:

    def __init__(self, model="llama-3.3-70b-versatile"):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.model = model

    def recommend(self, query, assessments):

        prompt = f"""
You are an SHL assessment recommendation assistant.

You MUST ONLY recommend assessments from the provided catalog.

Conversation:
{query}

Available Assessments:
{assessments}

Instructions:

- Recommend only assessments listed above.
- Explain briefly why each matches.
- Mention the skills evaluated.
- Never invent assessment names.
- Keep the answer concise and professional.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    def compare(self, question, assessments):

        prompt = f"""
You are an SHL assessment consultant.

Question:

{question}

Assessments:

{assessments}

Compare ONLY the assessments provided.

Include:

- Purpose
- Skills measured
- Differences
- When each should be chosen

Keep the comparison concise.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content