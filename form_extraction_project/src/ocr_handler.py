import pytesseract
from PIL import Image
import numpy as np
import os # Import the os module

class OCRExtractor:
    def extract_text(self, image: np.ndarray) -> str:
        """
        Performs OCR on a preprocessed image to extract text.
        """
        # Define the path to the Tesseract executable
        tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        
        # --- THIS IS THE DEBUGGING STEP ---
        # We will check if the file actually exists before we use it.
        if not os.path.exists(tesseract_path):
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"ERROR: Tesseract executable not found at: {tesseract_path}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            raise FileNotFoundError("Tesseract executable not found.")
        
        # This line tells the script the exact location of the Tesseract program.
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        try:
            # Convert the OpenCV image (NumPy array) to a PIL Image
            pil_image = Image.fromarray(image)
            
            # Use pytesseract to extract text
            text = pytesseract.image_to_string(pil_image)
            return text
        except Exception as e:
            print(f"Error during OCR extraction: {e}")
            return ""