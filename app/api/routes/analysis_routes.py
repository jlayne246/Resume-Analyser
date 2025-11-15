from fastapi import APIRouter, HTTPException, UploadFile, status, Request
from fastapi.responses import JSONResponse
# from app.api.controllers.analysis_controller import AnalysisController
from app.data.store_state import parsed_resumes
from app.data.analysis_results import analysis_results

router = APIRouter()

@router.post(
    "/execute"
)
async def execute_analysis(request: Request, career: str):
    resume_id = request.session.get("resume_id")
    try:
        try:
            resume_data = parsed_resumes.get(resume_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unable to retrieve resume data: {str(e)}"
            )
        
        # controller = AnalysisController()
        controller = None
    
        analysis = await controller.provide_analysis(
            resume_data,
            career
        )
        
        analysis_results[resume_id] = analysis
        
        return JSONResponse(content={"analysis": analysis, "details": resume_data}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print("Error occurred while generating analysis:", e)
        raise HTTPException(status_code=500, detail=str(e))