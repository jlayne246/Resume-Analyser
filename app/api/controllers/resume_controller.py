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
                # Log the first failure for debugging
                print(f"Primary model {model_version} failed: {e}")

                # Define a fallback model version
                fallback_version = 2 # Fallback to Gemini Flash 2.5

                try:
                    details = self.resume_service.ask_gemini_for_structured_resume(text, fallback_version)
                except Exception as e2:
                    # Log the fallback failure
                    print(f"Fallback model {fallback_version} also failed: {e2}")
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail="Gemini API failed for both primary and fallback versions."
                    )

                
            print("From Gemini: ", details)
            
            # Parse Gemini response as JSON
            try:
                data = json.loads(details)
            except json.JSONDecodeError as e:
                print("JSON parse error:", e)
                print("Offending snippet near:", details[e.pos-50:e.pos+50])
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