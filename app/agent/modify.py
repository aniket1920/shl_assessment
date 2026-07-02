ADD_WORDS = [
    "also",
    "include",
    "add"
]

REMOVE_WORDS = [
    "remove",
    "exclude",
    "drop"
]

def modification_type(query):
    q = query.lower()
    if any(w in q for w in ADD_WORDS):
        return "add"
    if any(w in q for w in REMOVE_WORDS):
        return "remove"
    return None