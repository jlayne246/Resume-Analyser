from similarity import compute_similarity

class FeatureBuilder:
    def __init__(self, resume_data, desired_role):
        self.resume_data = resume_data
        self.desired_role = desired_role
        self.features = {}
        
    def build_personal_features(self):
        self.features['has_name'] = bool(self.resume_data.first_name and self.resume_data.last_name)
        self.features['has_email'] = bool(self.resume_data.email)
        self.features['has_phone_number'] = bool(self.resume_data.phone)
        self.features['has_address'] = bool(self.resume_data.address)
    
    def build_summary_features(self):
        self.features['has_objective'] = bool(self.resume_data.objective)
        self.features['has_summary'] = bool(self.resume_data.summary)

        if self.resume_data.objective:
            self.features['objective_similarity'] = compute_similarity(self.resume_data.objective, self.desired_role)

        if self.resume_data.summary:
            self.features['summary_similarity'] = compute_similarity(self.resume_data.summary, self.desired_role)
            self.features['summary_length'] = len(self.resume_data.summary.split())

    def build_skill_features(self):
        self.features['num_hard_skills'] = len(self.resume_data.hard_skills or [])
        self.features['num_soft_skills'] = len(self.resume_data.soft_skills or [])

    def build_work_experience_features(self):
        # Need to rework Resume Model to have start_date and end_date as datetime objects before this can be implemented to create this feature
        # self.features['total_experience_years'] = self.calculate_experience_years()
        self.features['num_work_experiences'] = len(self.resume_data.work_experience or [])
        self.features['work_exp_similarity'] = []

        for work_exp in self.resume_data.get('work_experience', []):
            title = work_exp.title or ""
            company = work_exp.company or ""
            text = f"{title} {company}".strip()
            similarity_score = compute_similarity(text, self.desired_role)
            self.features['work_exp_similarity'].append(similarity_score)
        
        if self.features['work_exp_similarity']:
            self.features['avg_work_exp_similarity'] = sum(self.features['work_exp_similarity']) / len(self.features['work_exp_similarity'])
            self.features['max_work_exp_similarity'] = max(self.features['work_exp_similarity'])
        else:
            self.features['avg_work_exp_similarity'] = 0.0
            self.features['max_work_exp_similarity'] = 0.0

    def calculate_experience_years(self):
        # Need to rework Resume Model to have start_date and end_date as datetime objects before this can be implemented to create a feature
        return

    def build_education_features(self):
        self.features['num_education_entries'] = len(self.resume_data.education or [])
        self.features['has_education'] = bool(self.resume_data.education)

        similarities = []
        for edu in self.resume_data.education:
            degree = getattr(edu, 'degree', '') or ''
            field = getattr(edu, 'field_of_study', '') or ''
            text = f"{degree} {field}".strip()
            similarities.append(compute_similarity(text, self.desired_role))

        self.features['education_similarity'] = sum(similarities) / len(similarities) if similarities else 0.0

    def build_volunteer_features(self):
        self.features['num_volunteer_experiences'] = len(self.resume_data.volunteer_experience or [])
        self.features['has_volunteer_experience'] = bool(self.resume_data.volunteer_experience)
    
    def build_recognition_features(self):
        self.features['num_awards'] = len(self.resume_data.awards or [])
        self.features['has_awards'] = bool(self.resume_data.awards)
        self.features['num_publications'] = len(self.resume_data.publications or [])
        self.features['has_publications'] = bool(self.resume_data.publications)
        self.features['num_certifications'] = len(self.resume_data.certifications or [])
        self.features['has_certifications'] = bool(self.resume_data.certifications)

    def build_reference_features(self):
        self.features['num_references'] = len(self.resume_data.references or [])
        self.features['has_references'] = bool(self.resume_data.references),
    
    def build_features(self):
        self.build_personal_features()
        self.build_summary_features()
        self.build_skill_features()
        self.build_work_experience_features()
        self.build_education_features()
        self.build_volunteer_features()
        self.build_recognition_features()
        self.build_reference_features()
        return self.features