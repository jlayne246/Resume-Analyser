class RecommendationEngine:
    def __init__(self, ideal_features):
        self.actual = {}
        self.ideal = ideal_features
        self.recommendations = {
            "personal_recommendation": "",
            "summary_recommendation": "",
            "skill_recommendation": "",
            "work_experience_recommendation": "",
            "education_recommendation": "",
            "volunteer_experience_recommendation": "",
            "recognition_recommendation": "",
            "reference_recommendation": ""
        }

    def generate_recommendations(self):
        if not self.actual:
            raise ValueError("Actual features not set. Please set actual features before generating recommendations.")
        
        self.compare_group("personal_recommendation", [
            "has_name", "has_email", "has_phone_number", "has_address"
        ])
        self.compare_group("summary_recommendation", [
            "has_objective", "has_summary", "objective_similarity", "summary_similarity", "summary_length"
        ])
        self.compare_group("skill_recommendation", ["num_hard_skills", "num_soft_skills"])
        self.compare_group("work_experience_recommendation", ["num_work_experiences", "avg_work_exp_similarity", "max_work_exp_similarity"])
        self.compare_group("education_recommendation", ["num_education_entries", "has_education", "avg_education_similarity"])
        self.compare_group("volunteer_experience_recommendation", ["num_volunteer_experiences", "has_volunteer_experience"])
        self.compare_group("recognition_recommendation", [
            "num_awards", "has_awards",
            "num_publications", "has_publications",
            "num_certifications", "has_certifications"
        ])
        self.compare_group("reference_recommendation", ["num_references", "has_references"])
        return self.recommendations

    # ---------------- HELPER ---------------- #

    def compare_group(self, group_name, keys):
        messages = []

        for key in keys:
            if key not in self.actual or key not in self.ideal:
                continue

            actual = self.actual[key]
            ideal = self.ideal[key]

            # Boolean has_ feature → human readable
            if isinstance(ideal, bool) and key.startswith("has_") and actual != ideal:
                feature_name = key[4:]
                if ideal:
                    messages.append(f"should have {feature_name}")
                else:
                    messages.append(f"shouldn't have {feature_name}")

            # Numeric with range → ideal is [min,max]
            elif isinstance(ideal, list) and len(ideal) == 2:
                min_val, max_val = ideal
                if not (min_val <= actual <= max_val):
                    messages.append(f"{key}: expected between {min_val} and {max_val}, got {actual}")

            # Numeric single value
            elif isinstance(ideal, (int, float)):
                if actual != ideal:
                    messages.append(f"{key}: expected {ideal}, got {actual}")

        if messages:
            self.recommendations[group_name] = "; ".join(messages)
            
    def set_actual_features(self, actual_features):
        self.actual = actual_features
