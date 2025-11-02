from modules.gemini_integration.geminiClient import GeminiClient
class DetailExtractor:
    def __init__(self):
        self.query ="""
        Return structured resume data in JSON format for the following categories: namePresent, phoneNumberPresent, emailPresent, linkedInPresent, personalWebsitePresent, educationInstitutes, educationalDegrees, skills and companyNamesFromExperience following resume text:
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
            return self.client.askFlash2(self.query+resume)
        elif model == 2:
            return self.client.askFlash2_5(self.query+resume)