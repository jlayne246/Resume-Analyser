from app.modules.extraction.pdfTextExtractor import PDF
from app.modules.extraction.detailExtractor import DetailExtractor

class ResumeService:
    def __init__(self):
        # self.pdf_extractor = PDF()
        self.detail_extractor = DetailExtractor()
        
    async def extract_text_from_pdf(self, file_path):
        pdf = PDF(file_path)
        return pdf.extract_clean_text()
    
    def ask_gemini_for_structured_resume(self, resume_text, model_version):
        print("Asking Gemini for structured resume...")
        return self.detail_extractor.getStructuredResume(resume_text, model_version)