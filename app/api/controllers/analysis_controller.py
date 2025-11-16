# app/api/controllers/analysis_controller.py

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.api.services.analysis_service import AnalysisService

class AnalysisController:
    def __init__(self, resume_data, desired_role):
        self.analysis_service = AnalysisService(resume_data, desired_role)
        
    def provide_analysis(self):
        try: 
            recommendations = self.analysis_service.analyse_resume()
            return {"content": recommendations}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error analyzing resume: {str(e)}"
            )