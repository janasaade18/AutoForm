import pytesseract
from PIL import Image

print("--- Starting Tesseract Test ---")

try:
    # Create a blank black image. We don't need a real one.
    blank_image = Image.new('RGB', (100, 30), color = 'black')
    
    # Ask Tesseract to read the blank image.
    text = pytesseract.image_to_string(blank_image)
    
    print("\nSUCCESS! Tesseract is working correctly!")
    print(f"It read the blank image and returned: '{text}'")
    
except FileNotFoundError:
    print("\n--- TEST FAILED ---")
    print("CRITICAL ERROR: Tesseract was NOT found in the Windows PATH.")
    print("This confirms the PATH is the problem.")
    
except Exception as e:
    print(f"\n--- TEST FAILED WITH UNEXPECTED ERROR ---")
    print(e)

print("\n--- Test Complete ---")