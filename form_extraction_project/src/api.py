from fastapi import FastAPI, File, UploadFile
from .extractor import FormExtractor
import shutil
import os

app = FastAPI()
extractor = FormExtractor()

@app.post("/extract-form/")
async def extract_form_data(file: UploadFile = File(...)):
    """
    Accepts an image file, saves it temporarily, runs the extractor,
    and returns the extracted data.
    """
    # Create a temporary directory to store the uploaded file
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        extracted_data = extractor.extract(file_path)
        
    finally:
        # Ensure the temporary file is always cleaned up
        if os.path.exists(file_path):
            os.remove(file_path)
    
    return extracted_data