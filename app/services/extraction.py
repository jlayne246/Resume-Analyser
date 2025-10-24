from pyresparser import ResumeParser

def extract(path):
    data = ResumeParser(path).get_extracted_data()
    print(data)