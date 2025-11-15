# app/api/controllers/analysis_controller.py

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.api.services.analysis_service import AnalysisService

class AnalysisController:
    def __init__(self):
        self.analysis_service = AnalysisService()