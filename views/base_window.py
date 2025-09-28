from PySide6.QtWidgets import QMainWindow
from views.utils_view.view_position import center_on_screen


class BaseWindow(QMainWindow):
    def __init__(self, title, min_size=(960, 540), init_size=(1280, 720)):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(*min_size)
        self.resize(*init_size)
        center_on_screen(self)


