import json
from models.resume.ResumeModel import ResumeSchema
from modules.extraction.pdfTextExtractor import PDF
from modules.extraction.detailExtractor import DetailExtractor
from modules.analysis.similarity import compute_similarity
from modules.analysis.featureBuilder import FeatureBuilder
from dotenv import load_dotenv
load_dotenv()
print("Running tester.py")
if __name__ == "__main__":
    source = "samples/sampleJosh.pdf" #Path to a sample PDF file
    pdf=PDF(source)
    print("PDF loaded:", source)
    option = input("""
Pick an option\n
1: Count pages\n
2: Extract text\n
3: Extract clean text\n
4: Get Structured Resume\n
5: Check Similarity\n
6: Get Features from Structured Resume\n\n
Enter option number: """)
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
        option = input(
            """
Pick model to structure resume with:\n
1: Gemini Flash 2.0\n
2: Gemini Flash 2.5\n
\nEnter option number: """)
        if option not in ['1','2']:
            print("Invalid option selected.")
            exit(1)
        
        # LLM Prompt Builder and API Call
        details = detailExtractor.getStructuredResume(resume_text,int(option))
        
        # Validate and parse using Pydantic
        try:
            start = details.find('{')
            end = details.rfind('}')
            if start != -1 and end != -1:
                data = json.loads(details[start:end+1])
            else:
                data = json.loads(details)
            print(data)
            # data = json.loads(details[3:-3])
            # # resume = ResumeSchema(**data)
            # print(data)
        except Exception as e:
            print({"error": f"Parsing failed: {str(e)}", "raw_output": details})
    elif option == '5':
        print("Similarity Check between two texts")
        while True:
            text1 = input("Enter first text: ")
            text2 = input("Enter second text: ")
            score = compute_similarity(text1, text2)
            print(f"Similarity Score: {score}")
    elif option == '6':
        print("Feature Extraction from Structured Resume")
        # For testing, we will use a hardcoded structured resume JSON. Probably should save output from option 4 to a file and read from it here.
        