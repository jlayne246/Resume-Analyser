from app.models.resume.ResumeModel import ResumeSchema
from app.api.services.resume_service import ResumeService
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

import json

class ResumeController:
    def __init__(self):
        self.resume_service = ResumeService()
    
    async def parse_resume(self, file):
        try:
            print("Starting resume parsing process...")
            # Extract text from PDF
            try:
                text = await self.resume_service.extract_text_from_pdf(file)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f"Error extracting text from PDF: {str(e)}"
                )

            model_version = 1  # Default to Gemini Flash 2.0
            
            # Ask Gemini for structured resume
            try:
                details = self.resume_service.ask_gemini_for_structured_resume(text, model_version)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Gemini API returned no output."
                )
                
            print(details)
            
            # Parse Gemini response as JSON
            try:
                data = json.loads(details)
            except json.JSONDecodeError as e:
                raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Gemini returned invalid JSON: {str(e)}"
                    )
            
            # Validate schema using Pydantic
            try:
                resume = ResumeSchema(**data)
            except Exception as e:
                raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=f"Schema validation failed: {str(e)}"
                    )

            return {
                    "parsed_resume": resume.model_dump(),
                }
            
        except HTTPException as http_exc:
            raise http_exc
        
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Unexpected error: {str(e)}"
                )