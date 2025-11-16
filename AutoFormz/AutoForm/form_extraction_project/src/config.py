# Configuration for Form Extraction System

# Model Settings
MODEL_PATH = "./models/form_ner_v1"
CONFIDENCE_THRESHOLD = 0.7

# OCR Settings
OCR_LANGUAGE = "eng"
OCR_PSM_MODE = 6  # Assume uniform block of text

# Extraction Settings
ENABLE_NATURAL_LANGUAGE = True
ENABLE_LAYOUT_ANALYSIS = True
ENABLE_REGEX_FALLBACK = True

# Supported Field Types
SUPPORTED_FIELDS = [
    "FULL_NAME",
    "FIRST_NAME",
    "LAST_NAME",
    "EMAIL",
    "PHONE",
    "ADDRESS",
    "CITY",
    "STATE",
    "ZIP_CODE",
    "DATE_OF_BIRTH",
    "SSN",
    "GPA",
    "AGE",
    "COMPANY_NAME"
]

# API Settings
API_HOST = "0.0.0.0"
API_PORT = 8000
UPLOAD_DIR = "./uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
