from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class CategoryView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: green; border: none;")
        layout = QVBoxLayout(self)
        label = QLabel("Vista Home (home) - Index 0")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)