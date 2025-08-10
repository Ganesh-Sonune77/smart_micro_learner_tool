# runner.py — plays back recorded tasks (clicks + keypresses) with detailed step status and right-click support

import pyautogui
import time
import threading
from storage import TaskStorage

pyautogui.PAUSE = 0.5  # add pause between pyautogui actions

class TaskRunner:
    def __init__(self):
        self.running = False
        self._stop_event = threading.Event()
        self.storage = TaskStorage()

    def run(self, task_name):
        self.running = True
        self._stop_event.clear()

        task = self.storage.load_task(task_name)
        if not task:
            print(f"[Runner] Task '{task_name}' not found.")
            self.running = False
            return

        steps = task.get("steps", [])
        print(f"[Runner] Running {len(steps)} steps for task '{task_name}'")

        for i, action in enumerate(steps):
            if self._stop_event.is_set():
                print("[Runner] Task interrupted.")
                break

            action_type = action.get("type")
            print(f"[Runner] Step {i+1}/{len(steps)}: {action_type} -> {action}")

            if action_type == "click":
                x, y = action.get("x"), action.get("y")
                button = action.get("button", "left")
                print(f"[Runner] {button.capitalize()} click at ({x}, {y})")
                pyautogui.moveTo(x, y)
                if button == "right":
                    pyautogui.rightClick()
                else:
                    pyautogui.click()

            elif action_type == "keypress":
                key = action.get("key")
                print(f"[Runner] Pressing key: {key}")
                try:
                    if len(key) == 1:
                        pyautogui.typewrite(key)
                    else:
                        pyautogui.press(key.lower())
                except Exception as e:
                    print(f"[Runner] Error pressing key '{key}': {e}")

            time.sleep(0.4)  # more reliable timing

        self.running = False
        print("[Runner] Task completed.")

    def stop(self):
        self._stop_event.set()
        self.running = False
