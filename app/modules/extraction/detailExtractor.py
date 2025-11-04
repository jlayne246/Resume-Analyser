import json
from app.modules.gemini_integration.geminiClient import GeminiClient
from app.models.resume.ResumeModel import ResumeSchema

from typing import get_args, get_origin, Union

def example_json_from_model(model):
    print("Generating example JSON from model:", model.model_fields.items())
    example = {}

    for name, field in model.model_fields.items():
        annotation = field.annotation
        origin = get_origin(annotation)
        args = get_args(annotation)
        
        # Unwrap Optional[Something] (which is a Union[..., NoneType])
        if origin is Union and type(None) in args:
            # Replace annotation with the non-None inner type
            annotation = next(a for a in args if a is not type(None))
            origin = get_origin(annotation)
            args = get_args(annotation)

        # Handle list fields — add nested example if possible
        if origin == list and args:
            inner_type = args[0]
            # If it's a BaseModel (like WorkExperience, Education...)
            if hasattr(inner_type, "model_fields"):
                example[name] = [example_json_from_model(inner_type)]
            else:
                example[name] = []
            continue

        # Handle nested models directly
        if hasattr(annotation, "model_fields"):
            example[name] = example_json_from_model(annotation)
            continue

        # Your specific manual examples for known model names
        if "Publication" in str(annotation):
            example[name] = {
                "title": "string or null",
                "publisher": "string or null",
                "date": "string or null",
                "url": "string or null"
            }
        elif "Links" in str(annotation):
            example[name] = {
                "linkedin": "string or null",
                "personal_website": "string or null",
                "indeed": "string or null",
                "github": "string or null"
            }
        elif "Education" in str(annotation):
            example[name] = {
                "institution": "string or null",
                "location": "string or null",
                "degree": "string or null",
                "major": "string or null",
                "minor": "string or null",
                "start_date": "string or null",
                "end_date": "string or null",
                "details": "string or null",
                "gpa": "number or null",
                "relevant_coursework": []
            }
        elif "WorkExperience" in str(annotation):
            example[name] = {
                "company": "string or null",
                "location": "string or null",
                "title": "string or null",
                "start_date": "string or null",
                "end_date": "string or null",
                "description": "string or null"
            }
        elif "VolunteerExperience" in str(annotation):
            example[name] = {
                "organization": "string or null",
                "location": "string or null",
                "title": "string or null",
                "start_date": "string or null",
                "end_date": "string or null",
                "description": "string or null"
            }
        elif "Reference" in str(annotation):
            example[name] = {
                "name": "string or null",
                "title": "string or null",
                "company": "string or null",
                "mobile": "string or null",
                "email": "string or null"
            }
        elif annotation == bool:
            example[name] = "boolean (true or false)"
        elif annotation == str:
            example[name] = "string or null"
        elif annotation in (int, float):
            example[name] = "number or null"
        else:
            example[name] = None

    return example


schema_example = example_json_from_model(ResumeSchema)


# schema_template = ResumeSchema.model_json_schema()["properties"].keys()


class DetailExtractor:
    def __init__(self):
        self.query ="""
        Using these rules:
        - If data is missing, set field to null or an empty list.
        - Do not invent, infer, or guess any values.
        - Output only valid JSON. No commentary, no Markdown, no explanations.
        - For boolean fields: return only true or false.
        - For lists: return an empty list [] if nothing is found.
        - For strings: return null if missing.
        
        Return structured resume data in valid JSON object using the following schema and nothing else:
        {schema}
        
        For the following resume text:
        {resume_text}
        """
        self.client = GeminiClient()
    def getStructuredResume(self,resume:str,model:int=1)->str:
        """Returns a JSON of structured data about the resume.

        Args:
            resume (string): The resume text to be structured.
            model (int): The model to use for structuring the resume. 1 for Gemini Flash 2.0, 2 for Gemini Flash 2.5.
        Returns:
            dict: JSON with the following structure:
                {
                    "namePresent": bool,
                    "phoneNumberPresent": bool,
                    "emailPresent": bool,
                    "linkedInPresent": bool,
                    "personalWebsitePresent": bool,
                    "educationInstitutes": list[str],
                    "educationalDegrees": list[str],
                    "skills": list[str],
                    "companyNamesFromExperience": list[str]
                }
        """
        if model == 1:
            prompt = self.query.format(schema=json.dumps(schema_example, indent=2), resume_text=resume)
            print(prompt)
            return self.client.askFlash2(prompt)
        elif model == 2:
            return self.client.askFlash2_5(self.query+resume)
    def getQueryText(self)->str:
        return self.query
    