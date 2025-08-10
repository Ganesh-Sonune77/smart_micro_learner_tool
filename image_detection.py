# image_detection.py — Fixed and Log-enhanced

import cv2
import numpy as np
import pyautogui
import time

class ImageDetector:
    def __init__(self, threshold=0.8):
        self.threshold = threshold

    def locate_on_screen(self, template_path, timeout=5):
        print(f"[ImageDetector] Searching for image '{template_path}' with threshold {self.threshold}")
        start = time.time()
        try:
            template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
            if template is None:
                print(f"[ImageDetector] Failed to load image: {template_path}")
                return None
            th_h, th_w = template.shape[:2]

            while time.time() - start < timeout:
                screenshot = pyautogui.screenshot()
                screen_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                res = cv2.matchTemplate(screen_np, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)

                if max_val >= self.threshold:
                    x, y = max_loc
                    print(f"[ImageDetector] Match found at ({x}, {y}) with confidence {max_val}")
                    return x + th_w // 2, y + th_h // 2

                time.sleep(0.5)

        except Exception as e:
            print(f"[ImageDetector] Error: {e}")
        print("[ImageDetector] No match found within timeout.")
        return None

    def click_image(self, template_path, timeout=5):
        pos = self.locate_on_screen(template_path, timeout)
        if pos:
            pyautogui.click(*pos)
            print(f"[ImageDetector] Clicked image at {pos}")
            return True
        print(f"[ImageDetector] Image '{template_path}' not found for click")
        return False
