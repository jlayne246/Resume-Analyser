from fastapi import APIRouter, HTTPException, UploadFile, status, Request
from fastapi.responses import JSONResponse
from app.api.controllers.feedback_controller import FeedbackController
from app.data.feedback_generated import feedback_generated
from app.api.routes.analysis_routes import execute_analysis
import uuid

router = APIRouter()

# Calls the 
@router.post(
    "/generate"
)
async def generate_feedback(request: Request, career: str):
    resume_id = request.session.get("resume_id")
    try:
        try:
            details = await execute_analysis(request, career) # Placeholder for internal API call to analysis module
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unable to analyse resume data: {str(e)}"
            )
        
        controller = FeedbackController()
    
        feedback = await controller.provide_feedback(
            details.get("analysis")
        )
        
        feedback_generated[resume_id] = feedback
        
        return JSONResponse(content={"feedback": feedback, "details": details}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print("Error occurred while generating feedback:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get")
async def get_feedback(request: Request):
    resume_id = request.session.get("resume_id")
    generated_feedback = feedback_generated.get(resume_id, {})
    print("Retrieved generated feedback from session:", generated_feedback)
    return generated_feedback