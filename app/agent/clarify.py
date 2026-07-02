import re

SHORT_QUERIES = {
    "hi",
    "hello",
    "hey",
    "help",
    "assessment",
    "test",
    "recommend",
    "recommendation"
}

ROLE_HINTS = [
    "engineer",
    "developer",
    "analyst",
    "scientist",
    "consultant",
    "manager",
    "director",
    "executive",
    "graduate",
    "intern",
    "operator",
    "customer",
    "support",
    "finance",
    "accountant",
    "sales",
    "marketing",
    "healthcare",
    "administrator",
    "plant",
    "leader",
    "leadership",
    "technician",
    "call centre",
    "call center",
    "contact centre",
    "contact center"
]

HIRING_WORDS = [
    "hire",
    "hiring",
    "recruit",
    "recruiting",
    "looking for",
    "need",
    "screen",
    "screening",
    "candidate",
    "candidates",
    "role",
    "position",
    "vacancy"
]


def needs_clarification(query, state):

    query = query.lower().strip()

    if query in SHORT_QUERIES:
        return True, "Could you tell me which role you're hiring for?"

    if len(query.split()) <= 2:
        return True, "Could you tell me which role you're hiring for?"

    # Already know the role
    if state.role:
        return False, None

    # Looks like a genuine recruiter query
    if any(word in query for word in HIRING_WORDS):
        return False, None

    # Contains role keywords
    if any(role in query for role in ROLE_HINTS):
        return False, None

    return True, "Could you briefly describe the role you're hiring for?"