from PySide6.QtWidgets import QApplication
from ui.sandbox_window import SandboxWindow

from die_and_die_again.constants import __app_name__, __version__


class DieApp(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.setApplicationName(f"{__app_name__} {__version__}")
        self.main_window = SandboxWindow()

    def run(self):
        self.main_window.show()
        return self.exec()
