from fastapi import APIRouter, HTTPException, UploadFile, status, Request
from fastapi.responses import JSONResponse
from app.api.controllers.feedback_controller import FeedbackController
import uuid

router = APIRouter()

@router.post(
    "/generate"
)
async def generate_feedback(request: Request):
    return 0

@router.get("/get")
async def get_feedback(request: Request):
    return 0