import cv2
import numpy as np

class ImagePreprocessor:
    def preprocess(self, image_path: str) -> np.ndarray:
        """
        Loads an image and applies basic preprocessing steps for OCR.
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise FileNotFoundError(f"Image not found or unable to read at path: {image_path}")
            
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Apply a slight blur to reduce noise before thresholding
            blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
            # Adaptive thresholding is excellent for varying lighting conditions
            binary_image = cv2.adaptiveThreshold(
                blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            return binary_image
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            # Return an empty image on failure to prevent crashing the pipeline
            return np.array([[]], dtype=np.uint8)