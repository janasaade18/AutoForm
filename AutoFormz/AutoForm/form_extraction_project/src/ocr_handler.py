import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

class OCRExtractor:
    def extract_text(self, image: np.ndarray) -> str:
        """
        SIMPLIFIED OCR - focuses on clean text extraction
        """
        tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        
        if not os.path.exists(tesseract_path):
            print("❌ ERROR: Tesseract executable not found")
            return "Tesseract not found"
        
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        try:
            # Convert to PIL Image
            if len(image.shape) == 2:  # Grayscale
                pil_image = Image.fromarray(image)
            else:  # Color
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            # Use simple configuration for clean text
            text = pytesseract.image_to_string(pil_image, config='--psm 6')
            
            print(f"✅ OCR RAW RESULT: '{text}'")
            return text
            
        except Exception as e:
            print(f"❌ OCR Error: {e}")
            return f"OCR Error: {e}"