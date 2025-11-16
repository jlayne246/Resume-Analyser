from fastapi import APIRouter, HTTPException, UploadFile, status, Request
from fastapi.responses import JSONResponse
from app.api.controllers.analysis_controller import AnalysisController
from app.data.store_state import parsed_resumes
from app.data.analysis_results import analysis_results

router = APIRouter()

@router.post(
    "/execute"
)
def execute_analysis(request: Request, desired_role: str):
    resume_id = request.session.get("resume_id")
    try:
        try:
            resume_data = parsed_resumes.get(resume_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unable to retrieve resume data: {str(e)}"
            )
            
        print("Resume data for analysis:", resume_data)
        print("Desired role for analysis:", desired_role)
        
        controller = AnalysisController(resume_data,
            desired_role)
    
        analysis = controller.provide_analysis()
        
        analysis_results[resume_id] = analysis["content"]
        
        # return JSONResponse(content={"analysis": analysis, "details": resume_data}, status_code=status.HTTP_200_OK)
        return {"analysis": analysis["content"], "details": resume_data}
    except Exception as e:
        print("Error occurred while generating analysis:", e)
        raise HTTPException(status_code=500, detail=str(e))