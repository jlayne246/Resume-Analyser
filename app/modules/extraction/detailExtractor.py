from modules.gemini_integration.geminiClient import GeminiClient
class DetailExtractor:
    def __init__(self):
        self.query ="""
        Return structured resume data in JSON format for the following categories: namePresent, phoneNumberPresent, emailPresent, linkedInPresent, personalWebsitePresent, educationInstitutes, educationalDegrees, skills and companyNamesFromExperience following resume text:
        """
        self.client = GeminiClient()
    def getStructuredResume(self,resume:str,model:int=1)->str:
        if model == 1:
            return self.client.askFlash2(self.query+resume)
        elif model == 2:
            return self.client.askFlash2_5(self.query+resume)