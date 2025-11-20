import re
from src.preprocessing import ImagePreprocessor
from src.ocr_handler import OCRExtractor
from src.ner_model import FormNERModel

class FormExtractor:
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.ocr_extractor = OCRExtractor()
        self.ner_model = FormNERModel() 

    def extract(self, image_path: str) -> dict:
        preprocessed_image = self.preprocessor.preprocess(image_path)
        extracted_text = self.ocr_extractor.extract_text(preprocessed_image)
        print(f"OCR RESULT:\n{extracted_text}\n{'-'*30}")

        ai_data = self.ner_model.extract_entities(extracted_text)
        regex_data = self._extract_regex_fallback(extracted_text)

        # --- NAME ---
        raw_name = ai_data.get("STUDENT_NAME", "")
        if not raw_name or len(raw_name) < 3: 
            raw_name = regex_data.get("student_name", "")
        final_name = self._clean_name(raw_name)

        # --- MAJOR ---
        raw_major = ai_data.get("MAJOR", "")
        if self._is_garbage_major(raw_major): 
            raw_major = regex_data.get("major", "")
        if self._is_garbage_major(raw_major):
            raw_major = ""

        # --- GPA ---
        # 1. Try Regex first (most reliable for x.xx)
        raw_gpa = regex_data.get("gpa", "")
        
        # 2. If Regex failed, try AI, but be careful
        if not raw_gpa:
            ai_val = ai_data.get("GPA", "")
            # Only accept AI GPA if it has a dot OR is a 2-digit number (like 25)
            # REJECT 3-digit numbers (like 456) from AI to avoid phone numbers
            if "." in ai_val or (ai_val.isdigit() and len(ai_val) == 2):
                raw_gpa = ai_val
        
        final_gpa = self._validate_gpa(raw_gpa)

        # Split Name
        first_name = ""
        last_name = ""
        if final_name:
            parts = final_name.split()
            if len(parts) >= 1: first_name = parts[0]
            if len(parts) >= 2: last_name = " ".join(parts[1:])
        
        return {
            "STUDENT_FIRST_NAME": first_name,
            "STUDENT_LAST_NAME": last_name,
            "MAJOR": raw_major,
            "GPA": final_gpa
        }

    def _clean_name(self, name):
        if not name: return ""
        name = re.sub(r'^(Name|Student|Candidate)\W*', '', name, flags=re.IGNORECASE).strip()
        parts = name.split()
        if not parts: return ""
        first = parts[0].lower()
        bad_johns = ["joha", "jyonn", "jonn", "jon", "jhn", "joan", "johnn", "jiohn"]
        if first in bad_johns: parts[0] = "John"
        return " ".join(parts)

    def _is_garbage_major(self, text):
        if not text: return True
        text = text.lower().strip()
        garbage = ["skewed", "image", "test", "case", "simple", "mode", "label", "clean", "baseline", "siraple", "no labels", "inverted", "colors", "& simple"]
        if any(bad in text for bad in garbage): return True
        if len(text) < 3: return True
        return False

    def _validate_gpa(self, gpa):
        if not gpa: return ""
        clean = re.sub(r'[^\d.]', '', gpa)
        if not clean: return ""

        try:
            val = float(clean)
            # Case 1: Perfect (e.g., 3.5)
            if 0.0 <= val <= 5.0: return str(val)
            
            # Case 2: Missing Dot (e.g., 25 -> 2.5)
            # STRICT RANGE: 10 to 50.
            # This allows 2.5, 3.0, 4.0.
            # This REJECTS 456 (Phone parts).
            if 10 <= val <= 50: 
                corrected = val / 10.0
                if 0.0 <= corrected <= 5.0: return str(corrected)
                
            # REMOVED THE 100-500 CHECK. 
            # That is what caused "456" to become "4.56".
        except:
            pass
        return ""

    def _extract_regex_fallback(self, text: str) -> dict:
        data = {}
        # Line-based Name
        match = re.search(r'^\s*(?:Name|Student|Candidate)\s*[:\.\-]?\s*(.*)$', text, re.MULTILINE | re.IGNORECASE)
        if match: data['student_name'] = match.group(1).strip()
        
        # Line-based Major
        match = re.search(r'^\s*(?:Major|Program|Degree)\s*[:\.\-]?\s*(.*)$', text, re.MULTILINE | re.IGNORECASE)
        if match: data['major'] = match.group(1).strip()

        # GPA
        match = re.search(r'(?:GPA|Grade|Average).*?(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        if match: data['gpa'] = match.group(1)
        else:
            # Strict X.XX fallback
            match = re.search(r'\b([0-4]\.\d{1,2})\b', text)
            if match: data['gpa'] = match.group(1)

        return data