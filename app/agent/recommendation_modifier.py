def merge_recommendations(previous, new):
    seen = set()
    merged = []
    for item in previous + new:
        if item["name"] not in seen:
            merged.append(item)
            seen.add(item["name"])
    return merged

def remove_recommendations(previous, keyword):
    keyword = keyword.lower()
    return [
        r for r in previous
        if keyword not in r["name"].lower()
    ]