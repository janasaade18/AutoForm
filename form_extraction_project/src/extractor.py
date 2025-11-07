import re
from .preprocessing import ImagePreprocessor
from .ocr_handler import OCRExtractor
from .ner_model import FormNERModel

class FormExtractor:
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.ocr_extractor = OCRExtractor()
        self.ner_model = FormNERModel()

    def extract(self, image_path: str) -> dict:
        """
        Runs a flexible pipeline to extract student info from any document
        and maps it to the predefined C# application schema.
        This is robust and will not crash if fields are missing.
        """
        # 1. Get all the raw text from the image
        preprocessed_image = self.preprocessor.preprocess(image_path)
        extracted_text = self.ocr_extractor.extract_text(preprocessed_image)

        # 2. Use NER to find the person's name
        entities = self.ner_model.extract_entities(extracted_text)
        
        # 3. Use targeted keyword search for other specific fields
        major = self._find_field_value(extracted_text, ['Major', 'Field of Study'])
        gpa = self._find_field_value(extracted_text, ['GPA', 'Grade Point Average'])

        # 4. Map everything found to our C# application's schema.
        # This dictionary MUST contain the keys the C# app expects.
        final_data = {
            "STUDENT_FIRST_NAME": "",
            "STUDENT_LAST_NAME": "",
            "MAJOR": "",
            "GPA": ""
        }

        # Populate the dictionary only with the data we found
        if "PERSON" in entities:
            full_name = entities["PERSON"]
            name_parts = full_name.split()
            final_data["STUDENT_FIRST_NAME"] = name_parts[0] if len(name_parts) > 0 else ""
            final_data["STUDENT_LAST_NAME"] = name_parts[-1] if len(name_parts) > 1 else ""
        
        if major:
            final_data["MAJOR"] = major
        
        if gpa:
            # Clean up the GPA to only be the number (e.g., extract "3.8" from "GPA: 3.8/4.0")
            gpa_match = re.search(r'(\d\.\d+)', gpa)
            if gpa_match:
                final_data["GPA"] = gpa_match.group(1)

        return final_data

    def _find_field_value(self, text: str, keywords: list) -> str:
        """
        Searches for lines containing a keyword and extracts the value that follows.
        """
        for line in text.split('\n'):
            for keyword in keywords:
                # Regex to find the keyword (case-insensitive) followed by a separator and the value
                pattern = re.compile(rf'{re.escape(keyword)}[:\s]+(.*)', re.IGNORECASE)
                match = pattern.search(line)
                if match:
                    # Return the first value found, stripped of extra whitespace
                    return match.group(1).strip()
        return None # Return None if no keyword was found in any line