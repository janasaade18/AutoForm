from fastapi import FastAPI, File, UploadFile
from src.extractor import FormExtractor
import shutil
import os
import json

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
        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"🔄 API: Processing file: {file_path}")
        
        # Use your actual AI extractor
        extracted_data = extractor.extract(file_path)
        
        print(f"✅ API: Extraction completed. Data: {json.dumps(extracted_data, indent=2)}")
        
    except Exception as e:
        # If extraction fails, return error
        print(f"API: Extraction failed: {str(e)}")
        return {"error": f"Extraction failed: {str(e)}"}
        
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
    
    return extracted_data