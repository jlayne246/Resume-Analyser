import re
from pypdf import PdfReader

class PDF:
    def __init__(self, path):
        self.path = path

    def count_pages(self):
        reader = PdfReader(self.path)
        return len(reader.pages)
    
    def extract_text(self):
        reader = PdfReader(self.path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        return text
    
    def extract_clean_text(self):
        reader = PdfReader(self.path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        text = re.sub(r'[^\w\s]', '', text)  #Removes punctuation except for words and spaces
        text = re.sub(r'\s+', ' ', text)  #Replaces multiple spaces or tabs with a single space
        text = re.sub(r'\n+', ' ', text)  #Replaces newlines with a space
        
        return text.strip()