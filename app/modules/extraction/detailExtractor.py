from modules.gemini_integration.geminiClient import GeminiClient
from models.resume.ResumeModel import ResumeSchema

schema_json = ResumeSchema.schema_json(indent=2)

class DetailExtractor:
    def __init__(self):
        self.query ="""
        Using these rules:
        - If data is missing, set field to null or an empty list.
        - Do not invent, infer, or guess any values.
        - Output only valid JSON. No commentary, no Markdown, no explanations.
        
        Return structured resume data in valid JSON object using the following schema:
        {schema}
        
        For the following resume text:
        {resume_text}
        
        But if additional categories like certifications or awards exist, you may include them as extra keys with arrays of strings.
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
            prompt = self.query.format(schema=schema_json, resume_text=resume)
            return self.client.askFlash2(prompt)
        elif model == 2:
            return self.client.askFlash2_5(self.query+resume)
    def getQueryText(self)->str:
        return self.query