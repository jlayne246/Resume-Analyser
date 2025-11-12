from app.modules.gemini_integration.geminiClient import GeminiClient

class FeedbackGenerator:
    def __init__(self):
        self.query = """Provide feedback on a generic resume given the following details:
        
        Resume Details:
        {resume_details} 
        
        And on these particular points.
        
        Feedback Points:
        {feedback_points}
        """
        self.client = GeminiClient()
        
    def generate_feedback(self, resume_details, feedback_points, model):
        formatted_query = self.query.format(
            resume_details=resume_details,
            feedback_points=feedback_points
        )
        if model == 1:
            response = self.client.askFlash2(formatted_query)
        elif model == 2:
            response = self.client.askFlash2_5(formatted_query)
        return response