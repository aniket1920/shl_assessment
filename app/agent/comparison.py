COMPARE_WORDS = [
    "difference",
    "compare",
    "vs",
    "versus"
]

def is_comparison(query):
    q = query.lower()
    return any(word in q for word in COMPARE_WORDS)

def extract_products(query):
    products = []
    catalog = [
        "opq",
        "verify g",
        "verify numerical",
        "verify verbal",
        "verify interactive",
        "graduate scenarios",
        "java 8",
        "core java",
        "spring",
        "docker",
        "aws",
        "excel",
        "word"
    ]
    q = query.lower()
    for product in catalog:
        if product in q:
            products.append(product)
    return products