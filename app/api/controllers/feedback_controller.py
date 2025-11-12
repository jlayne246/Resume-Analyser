from app.api.services.feedback_service import FeedbackService
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

import json

class FeedbackController:
    def __init__(self):
        self.feedback_service = FeedbackService()
    
    def provide_feedback(self, resume_details, feedback_points):
        try:
            feedback = self.feedback_service.generate_feedback(resume_details, feedback_points)
            return JSONResponse(content={"feedback": feedback}, status_code=status.HTTP_200_OK)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating feedback: {str(e)}"
            )