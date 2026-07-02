class ConversationState:
    """
    Stores information gathered during the conversation.
    """

    def __init__(self):
        self.role = None
        self.domain = None 
        self.seniority = None
        self.skills = []
        self.assessment_types = []
        self.max_duration = None
        self.language = None
        self.previous_results = []
        self.finished = False

    def reset(self):
        self.__init__()

    def set_role(self, role):
        self.role = role
    
    def set_seniority(self, level):
        self.seniority = level 

    def add_skill(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)
    
    def add_assessment_type(self, assessment):
        if assessment not in self.assessment_types:
            self.assessment_types.append(assessment)

    def set_max_duration(self, minutes):
        self.max_duration = minutes

    def set_previous_results(self, results):
        self.previous_results = results

    def get_previous_results(self):
        return self.previous_results

    def clear_previous_results(self):
        self.previous_results = []

    def end(self):
        self.finished = True

    def __repr__(self):
        return (
            f"ConversationState("
            f"role={self.role}, "
            f"seniority={self.seniority}, "
            f"skills={self.skills}, "
            f"assessment_types={self.assessment_types}, "
            f"duration={self.max_duration}, "
            f"language={self.language}"
            f")"
        )