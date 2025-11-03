import json
from modules.gemini_integration.geminiClient import GeminiClient
from models.resume.ResumeModel import ResumeSchema

def example_json_from_model(model):
    example = {}
    for name, field in model.model_fields.items():
        if field.annotation == list or str(field.annotation).startswith("typing.List"):
            example[name] = []
        elif isinstance(field.default, model):
            example[name] = example_json_from_model(field.default)
        elif "Links" in str(field.annotation):
            example[name] = {
                "linkedin": "string or null", 
                "personal_website": "string or null",
                "indeed": "string or null", 
                "github": "string or null"
            }
        elif "Education" in str(field.annotation):
            example[name] = {
                "institution": "string or null",
                "location": "string or null",
                "degree": "string or null",
                "major": "string or null",
                "minor": "string or null",
                "start_date": "string or null",
                "end_date": "string or null",
                "details": "string or null",
                "gpa": "number or null"
            }
        elif "WorkExperience" in str(field.annotation):
            example[name] = {
                "company": "string or null",
                "location": "string or null",
                "job_title": "string or null",
                "start_date": "string or null",
                "end_date": "string or null",
                "description": "string or null"
            }
        elif "VolunteerExperience" in str(field.annotation):
            example[name] = {
                "entity": "string or null",
                "location": "string or null",
                "role": "string or null",
                "start_date": "string or null",
                "end_date": "string or null",
                "description": "string or null"
            }
        elif "Reference" in str(field.annotation):
            example[name] = {
                "name": "string or null",
                "title": "string or null",
                "organization": "string or null",
                "phone": "string or null",
                "email": "string or null"
            }
        elif field.annotation == bool:
            example[name] = "boolean (true or false)"
        elif field.annotation == str:
            example[name] = "string or null"
        elif field.annotation == int or field.annotation == float:
            example[name] = "number or null"
        else:
            example[name] = "null"
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
        
        Return structured resume data in valid JSON object using the following schema:
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
    