GREETING = [
    "hi",
    "hello",
    "hey"
]

GOODBYE = [
    "bye",
    "thanks",
    "thank you"
]

COMPARE = [
    "compare",
    "difference",
    "vs",
    "versus"
]

REFINE = [
    "also",
    "include",
    "add",
    "remove",
    "exclude",
    "drop",
    "replace",
    "instead"
]

RECOMMEND = [

    "recommend",
    "assessment",
    "test",
    "battery",

    "hire",
    "hiring",
    "recruit",
    "recruiting",

    "candidate",
    "screen",
    "screening",

    "engineer",
    "developer",
    "analyst",
    "manager",
    "director",
    "executive",

    "graduate",
    "intern",

    "sales",
    "finance",
    "marketing",

    "healthcare",

    "operator",

    "customer",

    "support",

    "leadership",

    "software",

    "python",

    "java",

    "rust",

    "sql",

    "aws",

    "docker"
]


def detect_intent(message):

    text = message.lower()

    if any(x in text for x in GOODBYE):
        return "goodbye"

    if any(x in text for x in COMPARE):
        return "compare"

    if any(x in text for x in REFINE):
        return "refine"

    if any(x in text for x in RECOMMEND):
        return "recommend"

    if any(x == text.strip() for x in GREETING):
        return "greeting"

    # Default assumption:
    # if the user writes a sentence, they probably want recommendations.
    return "recommend"