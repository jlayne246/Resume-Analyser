import re
import spacy
from pypdf import PdfReader
from transformers import BertTokenizer, BertForTokenClassification
import torch

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
        text = re.sub(r'\n+', ' ', text)  #Replaces newlines with a space Ney York -> NewYork
        
        return text
    
    
    def make_summary(self):
        nlp = spacy.load("en_core_web_sm")
        text = self.extract_text()
        doc = nlp(text)
        for ent in doc.ents:
            print(f"{ent.text} ({ent.label_})")

    def test_bert(self):
        tokenizer = BertTokenizer.from_pretrained('dbmdz/bert-large-cased-finetuned-conll03-english')
        model = BertForTokenClassification.from_pretrained('dbmdz/bert-large-cased-finetuned-conll03-english')
        
        text = self.extract_clean_text() #Text to categorize
        
        inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=2)

        # Map the predicted labels to human-readable entity names (e.g., PER, ORG, LOC)
        labels = model.config.id2label  # Mapping from label IDs to human-readable labels

        # Decode the tokens
        tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

        # Collect the tokens and their corresponding predicted labels
        entities = []
        for token, label_id in zip(tokens, predictions[0].tolist()):
            label = labels[label_id]
            # Ignore special tokens [CLS], [SEP], etc.
            if token not in tokenizer.all_special_tokens:
                entities.append((token, label))

        return entities