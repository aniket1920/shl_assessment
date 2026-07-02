VAGUE_TERMS = {
    "assessment",
    "assessments",
    "test",
    "tests",
    "need",
    "looking",
    "recommend",
    "recommendation",
    "hire",
    "hiring"
}

def latest_user_message(conversation):
    """
    Returns the latest message sent by the user.
    """
    for message in reversed(conversation):
        if message["role"] == "user":
            return message["content"]

    return ""

def is_vague(query):
    """
    Determine if a query lacks enough information.
    """
    words = query.lower().split()
    informative = [
        w
        for w in words
        if w not in VAGUE_TERMS
    ]
    return len(informative) < 2