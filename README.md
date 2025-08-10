Smart Macro Learner

A Python desktop application that learns your repeated PC tasks and automates them, with support for:

Mouse clicks & keyboard input recording

Image detection (OpenCV template matching)

OCR-based text detection & actions

Conditional task flows (if-then logic)

Floating, draggable '+' widget UI


Features

1. Add Task: Record a series of actions (3–4 repeats) and save as a named macro.


2. Run Task: Execute saved macros; icon turns green while running, click to stop.


3. Delete Task: Right-click on any saved task to delete with confirmation.


4. Smart Steps:

detect_image – click on screen template images.

ocr_click – find & click words on screen.

conditional – perform sub-steps when image/text conditions are met.




Installation

1. Clone the repository:

git clone https://github.com/yourusername/smart_macro_learner.git
cd smart_macro_learner


2. Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt



Usage

python main.py

A floating '+' icon appears. Drag it anywhere on screen.

Click '+' and select Add Task to record your steps (ESC to stop).

Right-click any saved task in the menu to delete.

Click a task name to run; icon turns green. Click again to stop.


Folder Details

tasks/saved_tasks.json: Stores user macros in JSON format.

icons/: Store template images (e.g., button screenshots) for detection.


Example Task JSON

See tasks/saved_tasks.json for structure:

{
  "MyMacro": {
    "steps": [
      { "type": "click", "x": 100, "y": 200, "time": 0.5 },
      { "type": "detect_image", "image": "icons/submit.png", "timeout": 5, "time": 1.2 },
      { "type": "ocr_click", "text": "Continue", "region": [0,0,800,600], "time": 2.0 }
    ]
  }
}

Contributing

Feel free to open issues or pull requests. For major changes, please discuss first.

License

Made By Ganesh Sonune 
