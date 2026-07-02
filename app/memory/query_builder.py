def build_search_query(state):
    """
    Convert conversation state into a semantic search query.
    Filters like duration/language are NOT added here.
    Those are handled later by apply_filters().
    """
    parts = []
    if state.role:
        parts.append(state.role)
    if state.seniority:
        parts.append(state.seniority)
    if state.domain:
        parts.append(state.domain)
    if state.skills:
        parts.extend(state.skills)
    return " ".join(parts).strip()