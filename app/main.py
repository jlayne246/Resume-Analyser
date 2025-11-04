import json
from models.resume.ResumeModel import ResumeSchema
from modules.extraction.pdfTextExtractor import PDF
from modules.extraction.detailExtractor import DetailExtractor
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    source = "samples/sampleJosh.pdf" #Path to a sample PDF file
    pdf=PDF(source)
    option = input("Pick an option\n1: Count pages\n2: Extract text\n3: Extract clean text\n4: Get Structured Resume\n\nEnter option number: ")
    if option == '1':
        print(f"Number of pages: {pdf.count_pages()}")
    elif option == '2':
        print("Extracted Text:")
        print(pdf.extract_text())
    elif option == '3':
        print("Extracted Text (clean):")
        print(pdf.extract_clean_text())
    elif option == '4':
        # Text Extraction (no cleaning as yet)
        resume_text = pdf.extract_text()
        
        detailExtractor = DetailExtractor()
        option = input("Pick model to structure resume with:\n1: Gemini Flash 2.0\n2: Gemini Flash 2.5\n\nEnter option number: ")
        if option not in ['1','2']:
            print("Invalid option selected.")
            exit(1)
        
        # LLM Prompt Builder and API Call
        details = detailExtractor.getStructuredResume(resume_text,int(option))
        
        # Validate and parse using Pydantic
        try:
            data = json.loads(details)
            resume = ResumeSchema(**data)
        except Exception as e:
            print({"error": f"Parsing failed: {str(e)}", "raw_output": details})
        