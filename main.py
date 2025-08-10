# main.py — Clean full implementation with all required features

import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QMenu, QAction,
    QInputDialog, QMessageBox
)
from PyQt5.QtGui import QCursor, QPainter, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSignal
from recorder import TaskRecorder
from runner import TaskRunner
from storage import TaskStorage


class FloatingWidget(QWidget):
    task_save_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(200, 80)

        self.button = QPushButton("+", self)
        self.button.setStyleSheet(self._style_idle())
        self.button.setFixedSize(60, 60)
        self.button.move(70, 10)
        self.button.clicked.connect(self.show_menu)

        self.menu = QMenu()
        self.add_task_action = QAction("Add Task", self)
        self.add_task_action.triggered.connect(self.add_task)
        self.menu.addAction(self.add_task_action)
        self.menu.addSeparator()

        self.recorder = TaskRecorder()
        self.runner = TaskRunner()
        self.storage = TaskStorage()

        self.task_actions = {}
        self.populate_tasks()

        self.mouse_drag_start = None
        self.is_dragging = False

        self.show_recording = False
        self.action_count = 0
        self.max_actions = 4
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        self.task_save_signal.connect(self._prompt_and_store)

    def _style_idle(self):
        return (
            "QPushButton { font-size: 28px; background-color: #444; color: white; border-radius: 30px; }"
            "QPushButton:hover { background-color: #666; }"
        )

    def _style_running(self):
        return (
            "QPushButton { font-size: 28px; background-color: green; color: white; border-radius: 30px; }"
            "QPushButton:hover { background-color: #5c8a00; }"
        )

    def populate_tasks(self):
        for name, act in self.task_actions.items():
            self.menu.removeAction(act)
        self.task_actions.clear()

        for name in self.storage.load_all_tasks():
            act = QAction(name, self)
            act.triggered.connect(lambda checked, n=name: self.run_task(n))
            self.menu.addAction(act)
            self.task_actions[name] = act

    def show_menu(self):
        self.menu.exec_(QCursor.pos())

    def add_task(self):
        QMessageBox.information(self, "Learning Mode", "Perform your task 3–4 times to train the macro.")
        self.recorder.actions = []
        self.action_count = 0
        self.show_recording = True
        self.timer.start(100)
        threading.Thread(target=self._record_and_save, daemon=True).start()

    def _record_and_save(self):
        print("[INFO] Recording started...")
        def count_actions():
            while self.show_recording:
                self.action_count = len(self.recorder.actions)
                QTimer.singleShot(0, self.update)
                time.sleep(0.1)

        threading.Thread(target=count_actions, daemon=True).start()
        actions = self.recorder.record()
        print("[INFO] Recording stopped.")
        self.show_recording = False
        self.timer.stop()
        self.task_save_signal.emit(actions)

    def _prompt_and_store(self, actions):
        name, ok = QInputDialog.getText(self, "Save Task", "Enter task name:")
        if ok and name:
            try:
                self.storage.save_task(name, actions)
                print(f"[INFO] Task '{name}' saved.")
                self.populate_tasks()
            except Exception as e:
                print(f"[ERROR] Saving failed: {e}")
                QMessageBox.critical(self, "Save Error", str(e))

    def run_task(self, name):
        if self.runner.running:
            print("[INFO] Stopping task.")
            self.runner.stop()
            self.button.setStyleSheet(self._style_idle())
        else:
            print(f"[INFO] Running task: {name}")
            self.button.setStyleSheet(self._style_running())
            threading.Thread(target=self._threaded_run, args=(name,), daemon=True).start()

    def _threaded_run(self, name):
        try:
            self.runner.run(name)
        except Exception as e:
            print(f"[ERROR] Task runner failed: {e}")
        self.button.setStyleSheet(self._style_idle())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_drag_start = event.globalPos()
            self.is_dragging = False

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mouse_drag_start:
            if not self.is_dragging:
                if (event.globalPos() - self.mouse_drag_start).manhattanLength() > 10:
                    self.drag_start_position = self.mouse_drag_start - self.frameGeometry().topLeft()
                    self.is_dragging = True
            if self.is_dragging:
                self.move(event.globalPos() - self.drag_start_position)

    def mouseReleaseEvent(self, event):
        self.mouse_drag_start = None
        self.drag_start_position = None
        self.is_dragging = False

    def paintEvent(self, event):
        if self.show_recording:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            width = self.width() - 20
            height = 8
            x = 10
            y = self.height() - 20

            painter.setBrush(QColor(100, 100, 100))
            painter.drawRect(x, y, width, height)

            fill = min(width, int((self.action_count / self.max_actions) * width))
            painter.setBrush(QColor(0, 200, 0))
            painter.drawRect(x, y, fill, height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = FloatingWidget()
    widget.show()
    sys.exit(app.exec_())
