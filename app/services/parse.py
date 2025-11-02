import spacy

nlp = spacy.load("en_core_web_sm")

class ResumeParser:
    def __init__(self, text):
        self.text = text
        self.doc = nlp(text)
        
    def return_tokens(self):
        return [token.text for token in self.doc]

    def extract_entities(self):
        entities = {}
        for ent in self.doc.ents:
            entities[ent.label_] = entities.get(ent.label_, []) + [ent.text]
        return entities