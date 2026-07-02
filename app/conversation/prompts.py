def build_context(conversation):
    """
    Convert conversation history into a prompt for the LLM.
    """
    lines = []
    for message in conversation:
        role = message["role"].capitalize()
        content = message["content"]
        lines.append(f"{role}: {content}")
    return "\n".join(lines)