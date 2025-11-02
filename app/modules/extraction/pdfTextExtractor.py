import re
from pypdf import PdfReader

class PDF:
    """A class to handle PDF text extraction and page counting.

    Attributes:
        path (str): The file path to the PDF document.
    """
    def __init__(self, path):
        """Initializes the PDF class with the given file path."""
        self.path = path

    def count_pages(self)->int:
        """Counts the number of pages in the PDF.
    
        Returns:
            int: Number of pages in the PDF.
        """
        reader = PdfReader(self.path)
        return len(reader.pages)
    
    def extract_text(self)->str:
        """Extracts text from the PDF.
    
        Returns:
            str: Text extracted from the PDF.
        """
        reader = PdfReader(self.path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        return text
    
    def extract_clean_text(self)->str:
        """Extracts and cleans text from the PDF.
        
        Returns:
            str: Cleaned text extracted from the PDF.
        """
        reader = PdfReader(self.path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        text = re.sub(r'[^\w\s]', '', text)  #Removes punctuation
        text = re.sub(r'\s+', ' ', text)  #Replaces multiple spaces or tabs with a single space
        text = re.sub(r'\n+', ' ', text)  #Replaces newlines with a space
        
        return text.strip()