from fastapi import APIRouter, HTTPException, UploadFile, status
from app.api.controllers.resume_controller import ResumeController

router = APIRouter()

@router.post(
        "/parse",
        status_code=status.HTTP_200_OK,
        summary="Parse and validate a resume",
        responses={
            200: {"description": "Resume parsed successfully"},
            400: {"description": "Bad input or missing file"},
            422: {"description": "Schema validation failed"},
            502: {"description": "Gemini API failure"},
            500: {"description": "Internal server error"},
        },
    )
async def parse_resume(file: UploadFile):
    try:
        content = await file.read()
        print(f"Received file: {file.filename}, size: {len(content)} bytes")
        
        controller = ResumeController()
        result = await controller.parse_resume(content)
        return result
    except Exception as e:
        print("Error occurred while parsing resume:", e)
        raise HTTPException(status_code=500, detail=str(e))
