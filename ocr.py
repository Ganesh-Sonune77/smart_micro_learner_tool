# ocr.py — Fixed and Log-Enhanced OCR Reader

import pytesseract
from PIL import ImageGrab
import cv2
import numpy as np
import time

# Optional: Set Tesseract path for Windows
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def pil_to_cv2(pil_image):
    open_cv_image = np.array(pil_image)
    return cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)


class OCRReader:
    def __init__(self, lang='eng'):
        self.lang = lang

    def find_text(self, text, region=None, timeout=5):
        print(f"[OCRReader] Searching for text: '{text}'")
        start = time.time()
        while time.time() - start < timeout:
            try:
                if region:
                    left, top, w, h = region
                    screenshot = ImageGrab.grab(bbox=(left, top, left + w, top + h))
                else:
                    screenshot = ImageGrab.grab()

                img_cv = pil_to_cv2(screenshot)
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

                data = pytesseract.image_to_data(thresh, lang=self.lang, output_type=pytesseract.Output.DICT)
                for i, word in enumerate(data['text']):
                    if word and text.lower() in word.lower():
                        x = data['left'][i]
                        y = data['top'][i]
                        w = data['width'][i]
                        h = data['height'][i]
                        cx = x + w // 2
                        cy = y + h // 2
                        print(f"[OCRReader] Found '{word}' at ({cx}, {cy})")
                        return cx, cy

            except Exception as e:
                print(f"[OCRReader] Error: {e}")
            time.sleep(0.5)

        print(f"[OCRReader] Text '{text}' not found within timeout.")
        return None