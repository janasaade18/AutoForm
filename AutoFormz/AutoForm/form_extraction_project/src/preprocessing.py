import cv2
import numpy as np
from scipy.ndimage import interpolation as inter

class ImagePreprocessor:
    def preprocess(self, image_path: str) -> np.ndarray:
        try:
            img = cv2.imread(image_path)
            if img is None: return np.zeros((100,100), dtype=np.uint8)

            img = self._remove_colored_lines(img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Check Dark Mode
            is_dark_mode = np.mean(gray) < 127

            # Scale 3x (Best balance)
            h, w = gray.shape
            scale = 3.0
            gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

            if is_dark_mode:
                gray = cv2.bitwise_not(gray)

            gray = self._correct_skew(gray)

            # --- BINARIZATION STRATEGY ---
            if is_dark_mode:
                # DIGITAL THICKENING MODE
                # We inverted. Text is 0 (Black). BG is 255 (White).
                # Edges are ~150 (Gray).
                # Threshold 190: Anything darker than 190 becomes Black (0).
                # This turns the gray edges into black, THICKENING the text.
                _, binary = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)
            else:
                # PAPER MODE (Otsu)
                blur = cv2.GaussianBlur(gray, (3,3), 0)
                _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            binary = cv2.copyMakeBorder(binary, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            return binary

        except Exception as e:
            print(f"Preprocessing error: {e}")
            return np.zeros((100, 100), dtype=np.uint8)

    def _remove_colored_lines(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red1, upper_red1 = np.array([0, 50, 50]), np.array([10, 255, 255])
        lower_red2, upper_red2 = np.array([170, 50, 50]), np.array([180, 255, 255])
        mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)
        lower_blue, upper_blue = np.array([90, 50, 50]), np.array([140, 255, 255])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask = mask_red + mask_blue
        kernel = np.ones((2,2), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
        return result

    def _correct_skew(self, image, delta=1, limit=5):
        try:
            def determine_score(arr, angle):
                data = inter.rotate(arr, angle, reshape=False, order=0)
                histogram = np.sum(data, axis=1, dtype=float)
                score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
                return histogram, score

            h, w = image.shape
            small = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
            thresh = cv2.threshold(small, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            scores = []
            angles = np.arange(-limit, limit + delta, delta)
            for angle in angles:
                _, score = determine_score(thresh, angle)
                scores.append(score)

            best_angle = angles[scores.index(max(scores))]
            if abs(best_angle) < 0.5: return image

            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            return rotated
        except:
            return image