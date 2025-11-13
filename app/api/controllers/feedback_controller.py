from app.api.services.feedback_service import FeedbackService
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

import json

class FeedbackController:
    def __init__(self):
        self.feedback_service = FeedbackService()
    
    def provide_feedback(self, resume_details):
        model = 1  # Default to Gemini Flash 2.0
        try:
            try:
                feedback = self.feedback_service.generate_feedback(resume_details, model)
            except Exception as e:
                print(f"Primary model {model} failed: {e}")

                fallback_model = 2  # Fallback to Gemini Flash 2.5

                try:
                    feedback = self.feedback_service.generate_feedback(resume_details, fallback_model)
                except Exception as e2:
                    print(f"Fallback model {fallback_model} also failed: {e2}")
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail="Gemini API failed for both primary and fallback versions."
                    )
            
            return JSONResponse(content={"feedback": feedback}, status_code=status.HTTP_200_OK)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating feedback: {str(e)}"
            )