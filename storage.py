# storage.py — saves and loads task JSON data

import json
import os

class TaskStorage:
    def __init__(self, filepath='saved_tasks.json'):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump({}, f)

    def save_task(self, name, actions):
        try:
            all_tasks = self.load_all_tasks()
            all_tasks[name] = {'steps': actions}
            with open(self.filepath, 'w') as f:
                json.dump(all_tasks, f, indent=2)
            print(f"[Storage] Task '{name}' saved.")
        except Exception as e:
            print(f"[Storage] Save error: {e}")

    def load_task(self, name):
        try:
            with open(self.filepath, 'r') as f:
                tasks = json.load(f)
            return tasks.get(name)
        except Exception as e:
            print(f"[Storage] Load task error: {e}")
            return None

    def load_all_tasks(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Storage] Load all error: {e}")
            return {}
