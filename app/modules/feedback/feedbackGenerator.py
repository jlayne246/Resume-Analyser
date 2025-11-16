from app.modules.gemini_integration.geminiClient import GeminiClient

feedback_points = {
        "score": 0,
        "recommendation":{
            "personal_recommendation":"",
            "summary_recommendation":"",
            "skill_recommendation":"",
            "work_experience_recommendation":"",
            "education_recommendation":"",
            "volunteer_experience_recommendation":"",
            "recognition_recommendation":"",
            "reference_recommendation":""
        }
}

class FeedbackGenerator:
    def __init__(self):
        self.query = """Provide feedback on a generic resume given the following details:
        
        Resume Details:
        {resume_details} 
        
        Using this particular schema for reference:
        {feedback_points}
        
        Here are the rules for providing feedback:
        1. Score the resume out of 10 based on overall quality, relevance, and completeness.
        2. Provide specific, actionable recommendations for improvement in each section of the resume as outlined in the schema.
        3. Be constructive and professional in your feedback.
        4. Return a only valid JSON object adhering to the provided schema. No commentary, no Markdown, no explanations.
        5. If there is nothing assigned for a particular point, return "This is fine as is" for that point.
        
        """
        self.client = GeminiClient()
        
    def generate_feedback(self, resume_details, model):
        formatted_query = self.query.format(
            resume_details=resume_details,
            feedback_points=feedback_points
        )
        if model == 1:
            response = self.client.askFlash2(formatted_query)
        elif model == 2:
            response = self.client.askFlash2_5(formatted_query)
        return response