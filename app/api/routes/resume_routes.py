from fastapi import APIRouter, HTTPException, UploadFile, status, Request
from fastapi.responses import JSONResponse
from app.api.controllers.resume_controller import ResumeController
import uuid
from app.data.store_state import parsed_resumes

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
async def parse_resume(request: Request, file: UploadFile):
    try:
        content = await file.read()
        print(f"Received file: {file.filename}, size: {len(content)} bytes")
        
        controller = ResumeController()
        # print(content)
        result = await controller.parse_resume(file.file)
        print("Parsed resume successfully:", result)

        # generate lightweight session key
        session_id = str(uuid.uuid4())
        parsed_resumes[session_id] = result["parsed_resume"]

        request.session["resume_id"] = session_id

        # 🔍 After saving
        # print("After saving session:", dict(request.session))
        return JSONResponse(status_code=status.HTTP_200_OK, content=session_id)
    except Exception as e:
        print("Error occurred while parsing resume:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get")
async def get_parsed_resume(request: Request):
    resume_id = request.session.get("resume_id")
    parsed_resume = parsed_resumes.get(resume_id, {})
    print("Retrieved parsed resume from session:", parsed_resume)
    return parsed_resume

@router.post("/update")
async def update_parsed_resume(request: Request):
    # ✅ 1. Get the session-bound resume ID
    resume_id = request.session.get("resume_id")
    if not resume_id:
        raise HTTPException(status_code=400, detail="No resume_id found in session")

    # ✅ 2. Parse incoming JSON data
    try:
        update_data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # ✅ 3. Ensure resume exists in memory
    if resume_id not in parsed_resumes:
        raise HTTPException(status_code=404, detail="Resume not found in session")

    # ✅ 4. Merge or replace the data (optional)
    parsed_resumes[resume_id] = update_data  # merges fields, doesn’t overwrite everything

    print(f"Updated parsed resume for session {resume_id}: {parsed_resumes[resume_id]}")

    # ✅ 5. Return a well-formed JSON response
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Resume updated successfully", "updated": parsed_resumes[resume_id]}
    )
