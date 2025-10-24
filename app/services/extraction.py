from pypdf import PdfReader

class PDF:
    def __init__(self, path):
        self.path = path
    def extract_text(self):
        with open(self.path, 'rb') as file:
            reader = PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
        return text
    def count_pages(self):
        with open(self.path, 'rb') as file:
            reader = PdfReader(file)
            return len(reader.pages)
