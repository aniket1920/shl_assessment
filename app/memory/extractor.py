import re

SKILLS = [

    "python",
    "java",
    "spring",
    "spring boot",
    "sql",
    "docker",
    "aws",
    "angular",
    "react",
    "javascript",
    "c++",
    "linux",
    "excel",
    "word",
    "sales",
    "leadership",
    "finance"

]

ASSESSMENTS = {
    "personality": "Personality",
    "cognitive": "Cognitive",
    "ability": "Ability",
    "knowledge": "Knowledge",
    "simulation": "Simulation",
    "behavior": "Behavior",
    "behaviour": "Behavior",
    "situational": "Situational Judgement"
}

def extract_duration(text):
    match = re.search(r"(\d+)\s*minutes?", text.lower())
    if match:
        return int(match.group(1))
    return None

def extract_skills(text):
    text = text.lower()
    skills = []
    for skill in SKILLS:
        if skill in text:
            skills.append(skill.title())
    return skills

def extract_assessment_types(text):
    text = text.lower()
    found = []
    for key,value in ASSESSMENTS.items():
        if key in text:
            found.append(value)
    return list(set(found))

def extract_seniority(text):
    text = text.lower()
    levels = [
        "graduate",
        "entry",
        "junior",
        "mid",
        "senior",
        "manager",
        "director",
        "executive"
    ]
    for level in levels:
        if level in text:
            return level.title()
    return None

ROLES = [
    "engineer",
    "developer",
    "analyst",
    "scientist",
    "consultant",
    "manager",
    "sales",
    "marketing",
    "finance",
    "accountant",
    "support",
    "customer service",
    "call center",
    "operator",
    "technician",
    "administrator",
    "assistant",
    "graduate",
    "intern"
    ]

def extract_role(text):
    lower = text.lower()

    # First check for common role keywords
    for role in ROLES:
        if role in lower:
            return text.strip().title()

    # Otherwise clean recruiter wording
    remove = [
        "we're",
        "we are",
        "looking for",
        "need",
        "hiring",
        "hire",
        "candidate",
        "candidates",
        "assessment",
        "assessments",
        "test",
        "tests",
        "screening",
        "screen",
        "also",
        "include",
        "remove",
        "add",
    ]

    cleaned = lower

    for word in remove:
        cleaned = cleaned.replace(word, " ")

    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if len(cleaned) > 5:
        return cleaned.title()

    return None


def update_state(state, text):
    role = extract_role(text)
    if role:
        state.set_role(role)
    seniority = extract_seniority(text)
    if seniority:
        state.set_seniority(seniority)
    duration = extract_duration(text)
    if duration:
        state.set_max_duration(duration)
    for skill in extract_skills(text):
        state.add_skill(skill)
    for assessment in extract_assessment_types(text):
        state.add_assessment_type(assessment)
    return state

