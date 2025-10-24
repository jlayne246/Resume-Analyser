from pypdf import PdfReader

class PDF:
    def __init__(self, path):
        self.path = path

    def extract_text(self):
        reader = PdfReader(self.path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        return text
    
    def count_pages(self):
        reader = PdfReader(self.path)
        return len(reader.pages)
