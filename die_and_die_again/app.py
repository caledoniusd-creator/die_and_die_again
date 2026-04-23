import sys
from PySide6.QtWidgets import QApplication
from ui.sandbox_window import SandboxWindow

class DieApp(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.setApplicationName("Die and Die Again")
        self.main_window = SandboxWindow()

    def run(self):
        self.main_window.show()
        return self.exec()
