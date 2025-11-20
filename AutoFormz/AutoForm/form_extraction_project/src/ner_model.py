import spacy
import os

class FormNERModel:
    def __init__(self, model_dir="models/custom_form_model"):
        self.model_path = model_dir
        
        # 1. Load Custom Model (The Specialist)
        if os.path.exists(self.model_path):
            print(f"Loading CUSTOM model from {self.model_path}...")
            self.custom_nlp = spacy.load(self.model_path)
        else:
            print("Custom model not found. Initialization failed.")
            self.custom_nlp = None

        # 2. Load Standard English Model (The Validator)
        # We use this to double-check if a name is actually a person
        try:
            print("Loading Standard English model for validation...")
            self.validator_nlp = spacy.load("en_core_web_sm")
        except:
            print("Warning: Standard model not found. Run 'python -m spacy download en_core_web_sm'")
            self.validator_nlp = None

    def extract_entities(self, text: str) -> dict:
        if not self.custom_nlp:
            return {}

        doc = self.custom_nlp(text)
        entities = {}

        print("AI Scanning text...")

        for ent in doc.ents:
            clean_text = ent.text.strip().replace("\n", " ")
            label = ent.label_

            # --- LOGIC 2: THE COUNCIL OF MODELS (Validation) ---
            # If the Custom Model finds a NAME, check with the Standard Model
            if label == "STUDENT_NAME" and self.validator_nlp:
                if not self._is_valid_person(clean_text):
                    print(f"⚠️ REJECTED Name '{clean_text}': Standard Model says it's not a person.")
                    continue  # Skip this entity
            # ---------------------------------------------------

            if label not in entities:
                entities[label] = clean_text
                print(f"Accepted {label}: {clean_text}")

        return entities

    def _is_valid_person(self, text: str) -> bool:
        """
        Asks the standard English model: 'Is this text a Person?'
        """
        doc = self.validator_nlp(text)
        # If the standard model finds a PERSON entity in this text, it's valid.
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return True
        
        # Fallback: If text is two capitalized words (e.g. SEFEG K), allow it slightly more often
        # But 'Inverted Colors' usually isn't tagged as PERSON by standard spacy.
        return False