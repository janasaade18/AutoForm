import spacy

class FormNERModel:
    def __init__(self, model_name="en_core_web_sm"):
        """
        Loads a spaCy NER model.
        """
        self.nlp = spacy.load(model_name)

    def extract_entities(self, text: str) -> dict:
        """
        Extracts named entities from the given text.
        """
        doc = self.nlp(text)
        entities = {}
        # Find the first person entity and stop, as a form usually refers to one person.
        for ent in doc.ents:
            if ent.label_ == "PERSON" and "PERSON" not in entities:
                entities[ent.label_] = ent.text
        return entities