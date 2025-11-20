import pytesseract
import numpy as np
import os

class OCRExtractor:
    def extract_text(self, image: np.ndarray) -> str:
        # 1. Verify Tesseract Path
        tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if not os.path.exists(tesseract_path):
            print("CRITICAL ERROR: Tesseract.exe not found. Please install it.")
            return ""
            
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        try:
            # --- THE FIX ---
            # I removed the 'tessedit_char_whitelist' section.
            # It contained nested quotes that caused the "No closing quotation" error.
            # --psm 6: Assume a single uniform block of text.
            # --oem 3: Use default OCR engine.
            config = r'--oem 3 --psm 6'
            
            # Run OCR
            text = pytesseract.image_to_string(image, config=config)
            
            return text
            
        except Exception as e:
            # This prints the actual error if something else breaks
            print(f"OCR Error: {e}")
            return ""