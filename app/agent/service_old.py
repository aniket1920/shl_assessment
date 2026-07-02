from app.agent.intent import detect_intent
from app.agent.clarify import needs_clarification

from app.memory.state import ConversationState
from app.memory.extractor import update_state
from app.memory.query_builder import build_search_query

from app.retrieval.filter import apply_filters
from app.agent.followup import is_follow_up
from app.agent.modify import modification_type
from app.agent.recommendation_modifier import (
    merge_recommendations,
    remove_recommendations
)
from app.agent.comparison import (
    is_comparison,
    extract_products
)

class AgentService:

    def __init__(self, retriever, embedder, llm):
        self.retriever = retriever
        self.embedder = embedder
        self.llm = llm
        self.state = ConversationState()

    def chat(self, conversation):

        # ---------------------------------
        # Latest user message
        # ---------------------------------

        query = conversation[-1]["content"]

        # Detect intent first
        intent = detect_intent(query)
        if is_comparison(query):

            products = extract_products(query)

            search_query = " ".join(products)

            embedding = self.embedder.encode([search_query])

            results = self.retriever.search(
                query=search_query,
                query_embedding=embedding,
                top_k=2
            )

        # Update memory
        update_state(self.state, query)

        # ---------------------------------
        # Greeting
        # ---------------------------------

        if intent == "greeting":
            return {
                "reply": "Hello! How can I help you choose SHL assessments today?",
                "recommendations": []
            }

        # ---------------------------------
        # Goodbye
        # ---------------------------------

        if intent == "goodbye":
            return {
                "reply": "You're welcome. Let me know if you need another assessment recommendation.",
                "recommendations": []
            }

        # ---------------------------------
        # Recommendation Intent
        # ---------------------------------

        if intent == "recommend":

            clarify, question = needs_clarification(query)

            if clarify:
                return {
                    "reply": question,
                    "recommendations": []
                }
            follow_up = is_follow_up(query)
            if follow_up:
                previous = self.state.get_previous_results()
                action = modification_type(query)
                if action == "remove":
                    keyword = query.split()[-1]

                    results = remove_recommendations(
                        previous,
                        keyword
                    )

                elif action == "add":

                    search_query = build_search_query(self.state)

                    if "personality" in query.lower():
                        search_query += " personality"

                    if "cognitive" in query.lower():
                        search_query += " cognitive"

                    if "situational" in query.lower():
                        search_query += " situational"

                    embedding = self.embedder.encode([search_query])

                    new_results = self.retriever.search(
                        query=search_query,
                        query_embedding=embedding,
                        top_k=5
                    )

                    new_results = apply_filters(
                        new_results,
                        self.state
                    )

                    results = merge_recommendations(
                        previous,
                        new_results
                    )

                else:

                    results = previous

            else:

                search_query = build_search_query(self.state)

                query_embedding = self.embedder.encode([search_query])

                results = self.retriever.search(
                    query=search_query,
                    query_embedding=query_embedding,
                    top_k=10
                )

                results = apply_filters(results, self.state)


            # ---------------------------------
            # Build search query from memory
            # ---------------------------------

            search_query = build_search_query(self.state)

            print("=" * 60)
            print("Conversation State")
            print(self.state)
            print()
            print("Semantic Search Query")
            print(search_query)
            print("=" * 60)

            # ---------------------------------
            # Embed query
            # ---------------------------------

            query_embedding = self.embedder.encode([search_query])

            # ---------------------------------
            # Retrieve
            # ---------------------------------

            results = self.retriever.search(
                query=search_query,
                query_embedding=query_embedding,
                top_k=10
            )

            # ---------------------------------
            # Apply conversational filters
            # ---------------------------------

            results = apply_filters(results, self.state)

            # ---------------------------------
            # Save previous results
            # ---------------------------------

            self.state.set_previous_results(results)

            # ---------------------------------
            # Build assessment context
            # ---------------------------------

            assessment_text = ""

            for result in results:

                assessment_text += f"""
Name: {result['name']}
Assessment Type: {result['assessment_type']}
Job Level: {result['job_level']}
Duration: {result['duration']}
URL: {result['url']}

"""

            # ---------------------------------
            # Ask LLM
            # ---------------------------------

            explanation = self.llm.recommend(
                query=search_query,
                assessments=assessment_text
            )

            return {
                "reply": explanation,
                "recommendations": results
            }

        # ---------------------------------
        # Unknown Intent
        # ---------------------------------

        return {
            "reply": "I'm not sure I understood that. Could you tell me more about the role or assessments you're looking for?",
            "recommendations": []
        }