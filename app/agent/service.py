from app.agent.intent import detect_intent
from app.agent.clarify import needs_clarification
from app.agent.followup import is_follow_up
from app.agent.modify import modification_type
from app.agent.comparison import is_comparison, extract_products
from app.agent.recommendation_modifier import (
    merge_recommendations,
    remove_recommendations,
)
from app.memory.state import ConversationState
from app.memory.extractor import update_state
from app.memory.query_builder import build_search_query
from app.retrieval.filter import apply_filters


class AgentService:

    def __init__(self, retriever, embedder, llm):
        self.retriever = retriever
        self.llm = llm
        self.state = ConversationState()

    def chat(self, conversation):
        query = conversation[-1]["content"].strip()
        intent = detect_intent(query)

        if intent == "greeting":
            return {
                "reply": "Hello! How can I help you choose SHL assessments today?",
                "recommendations": []
            }

        if intent == "goodbye":
            return {
                "reply": "You're welcome. Let me know if you need another assessment recommendation.",
                "recommendations": []
            }

        if is_comparison(query):
            return self.handle_comparison(query)

        return self.handle_recommendation(query)

    def handle_comparison(self, query):

        products = extract_products(query)
        search_query = " ".join(products)

        results = self.retriever.search(
            query=search_query,
            top_k=2
        )

        comparison_text = ""

        for r in results:
            comparison_text += (
                f"Name: {r.get('name','')}\n"
                f"Assessment Type: {r.get('assessment_type','')}\n"
                f"Job Level: {r.get('job_level','')}\n"
                f"Duration: {r.get('duration','')}\n"
                f"URL: {r.get('url','')}\n\n"
            )

        return {
            "reply": self.llm.compare(query, comparison_text),
            "recommendations": results,
        }

    def handle_recommendation(self, query):

        follow_up = is_follow_up(query)

        if not follow_up:
            self.state = ConversationState()

        update_state(self.state, query)

        clarify, question = needs_clarification(query, self.state)

        if clarify:
            return {
                "reply": question,
                "recommendations": []
            }

        if follow_up and self.state.get_previous_results():

            previous = self.state.get_previous_results()
            action = modification_type(query)

            if action == "remove":

                results = remove_recommendations(
                    previous,
                    query.split()[-1]
                )

            elif action == "add":

                search_query = build_search_query(self.state)

                lower = query.lower()

                if "personality" in lower:
                    search_query += " personality"

                if "cognitive" in lower:
                    search_query += " cognitive"

                if "situational" in lower:
                    search_query += " situational"

                new_results = self.retriever.search(
                    query=search_query,
                    top_k=3
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

            results = self.retriever.search(
                query=search_query if search_query else query,
                top_k=5
            )

            results = apply_filters(
                results,
                self.state
            )

        self.state.set_previous_results(results)

        assessment_text = ""

        for r in results:
            assessment_text += (
                f"Name: {r.get('name','')}\n"
                f"Assessment Type: {r.get('assessment_type','')}\n"
                f"Job Level: {r.get('job_level','')}\n"
                f"Duration: {r.get('duration','')}\n"
                f"URL: {r.get('url','')}\n\n"
            )

        return {
            "reply": self.llm.recommend(
                build_search_query(self.state),
                assessment_text
            ),
            "recommendations": results,
        }