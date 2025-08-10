# recorder.py — captures mouse clicks and keyboard presses with ESC to stop + right-click support

import time
from pynput import mouse, keyboard

class TaskRecorder:
    def __init__(self):
        self.actions = []
        self.recording = False

    def record(self):
        self.recording = True
        self.actions.clear()

        def on_click(x, y, button, pressed):
            if pressed:
                print(f"[Recorder] Click at ({x}, {y}) with {button.name}")
                self.actions.append({
                    'type': 'click',
                    'x': x,
                    'y': y,
                    'button': button.name,
                    'time': time.time()
                })

        def on_press(key):
            if key == keyboard.Key.esc:
                print("[Recorder] ESC pressed, stopping...")
                self.recording = False
                return False  # stop keyboard listener
            try:
                if hasattr(key, 'char') and key.char:
                    print(f"[Recorder] Key: {key.char}")
                    self.actions.append({
                        'type': 'keypress',
                        'key': key.char,
                        'time': time.time()
                    })
                else:
                    print(f"[Recorder] Special key: {key}")
                    self.actions.append({
                        'type': 'keypress',
                        'key': str(key).split('.')[-1],
                        'time': time.time()
                    })
            except Exception as e:
                print(f"[Recorder] Error: {e}")

        with mouse.Listener(on_click=on_click) as ml, \
             keyboard.Listener(on_press=on_press) as kl:
            while self.recording:
                time.sleep(0.1)

        return self.actions
