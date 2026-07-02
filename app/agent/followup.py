FOLLOW_UP_KEYWORDS = [
    "also",
    "include",
    "add",
    "remove",
    "exclude",
    "replace",
    "instead",
    "shorter",
    "under",
    "less than",
    "longer",
    "language",
    "english",
    "spanish",
    "french",
    "personality",
    "cognitive",
    "situational",
    "simulation"
]


def is_follow_up(query):

    query = query.lower()

    return any(word in query for word in FOLLOW_UP_KEYWORDS)