import re
from src.preprocessing import ImagePreprocessor
from src.ocr_handler import OCRExtractor

class FormExtractor:
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.ocr_extractor = OCRExtractor()

    def extract(self, image_path: str) -> dict:
        # 1. Get ALL text from image
        preprocessed_image = self.preprocessor.preprocess(image_path)
        extracted_text = self.ocr_extractor.extract_text(preprocessed_image)

        print(f"🔍 DEBUG: OCR Text: '{extracted_text}'")

        # 2. EXTRACT EVERYTHING DYNAMICALLY - NO ORDER DEPENDENCY
        all_data = self._extract_all_fields(extracted_text)
        
        result = {
            "STUDENT_FIRST_NAME": all_data.get('first_name', ''),
            "STUDENT_LAST_NAME": all_data.get('last_name', ''),
            "MAJOR": all_data.get('major', ''),
            "GPA": all_data.get('gpa', '')
        }

        print(f"✅ EXTRACTION RESULT: {result}")
        return result

    def _extract_all_fields(self, text: str) -> dict:
        """ULTRA DYNAMIC - EXTRACTS ALL FIELDS REGARDLESS OF ORDER"""
        data = {}
        
        # SPLIT INTO LINES AND PROCESS EACH ONE
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # CHECK EACH LINE FOR ANY FIELD PATTERN
            self._check_line_for_fields(line, data)
        
        return data

    def _check_line_for_fields(self, line: str, data: dict):
        """CHECK A SINGLE LINE FOR ANY FIELD - ORDER DOESN'T MATTER"""
        
        # NAME PATTERNS (flexible)
        name_match = re.search(r'name\s*:?\s*([a-zA-Z]+)(?:\s+([a-zA-Z]+))?', line, re.IGNORECASE)
        if name_match and not data.get('first_name'):
            first = name_match.group(1).capitalize()
            last = name_match.group(2).capitalize() if name_match.group(2) else ""
            data['first_name'] = first
            if last:
                data['last_name'] = last

        # FIRST NAME PATTERNS
        first_match = re.search(r'first\s*:?\s*([a-zA-Z]+)', line, re.IGNORECASE)
        if first_match and not data.get('first_name'):
            data['first_name'] = first_match.group(1).capitalize()

        # LAST NAME PATTERNS  
        last_match = re.search(r'last\s*:?\s*([a-zA-Z]+)', line, re.IGNORECASE)
        if last_match and not data.get('last_name'):
            data['last_name'] = last_match.group(1).capitalize()

        # MAJOR PATTERNS
        major_match = re.search(r'major\s*:?\s*(.+)', line, re.IGNORECASE)
        if major_match and not data.get('major'):
            major = major_match.group(1).strip()
            major = re.sub(r'[^\w\s]', '', major).strip()
            if major:
                data['major'] = major.title()

        # GPA PATTERNS
        gpa_match = re.search(r'gpa\s*:?\s*([0-9]\.[0-9]+)', line, re.IGNORECASE)
        if gpa_match and not data.get('gpa'):
            data['gpa'] = gpa_match.group(1)

        # STANDALONE GPA (anywhere in line)
        gpa_standalone = re.search(r'\b([0-4]\.[0-9]+)\b', line)
        if gpa_standalone and not data.get('gpa'):
            data['gpa'] = gpa_standalone.group(1)

        # STANDALONE NAMES (if no labels found)
        if not data.get('first_name'):
            words = re.findall(r'\b[a-zA-Z]+\b', line)
            if len(words) >= 2 and len(words[0]) > 2:
                data['first_name'] = words[0].capitalize()
                if len(words) >= 2:
                    data['last_name'] = words[1].capitalize()

    def _extract_names(self, text: str):
        """DEPRECATED - NOW USING ULTRA DYNAMIC APPROACH"""
        return ("", "")

    def _extract_major(self, text: str) -> str:
        """DEPRECATED - NOW USING ULTRA DYNAMIC APPROACH"""
        return ""

    def _extract_gpa(self, text: str) -> str:
        """DEPRECATED - NOW USING ULTRA DYNAMIC APPROACH"""
        return ""