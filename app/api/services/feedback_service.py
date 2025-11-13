import app.modules.feedback.feedbackGenerator as feedbackGenerator

class FeedbackService:
    def __init__(self):
        self.feedback_generator = feedbackGenerator.FeedbackGenerator()
        
    def generate_feedback(self, resume_details, model):
        return self.feedback_generator.generate_feedback(resume_details, model)