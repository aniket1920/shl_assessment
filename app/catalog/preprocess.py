from typing import Dict
import re

def extract_duration_minutes(duration: str):
    """
    Extract duration in minutes from strings like:
    '25 minutes'
    '7 minutes'
    Returns None if unavailable.
    """
    if not duration:
        return None
    match = re.search(r"(\d+)", duration)
    if match:
        return int(match.group(1))
    return None

def is_report(name: str):
    if not name:
        return False
    return "report" in name.lower()

def build_search_document(assessment: Dict):

    fields = [
        ("Name", assessment.get("name")),
        ("Description", assessment.get("description")),
        ("Assessment Type", ", ".join(assessment.get("keys", []))),
        ("Job Levels", ", ".join(assessment.get("job_levels", []))),
        ("Languages", ", ".join(assessment.get("languages", []))),
        ("Duration", assessment.get("duration")),
        ("Adaptive", assessment.get("adaptive")),
        ("Remote", assessment.get("remote")),
    ]
    text = []
    for label, value in fields:
        if value:
            text.append(f"{label}: {value}")
    return "\n".join(text)