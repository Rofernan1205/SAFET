import os
import sys
from views.utils_view.add_images import get_images_path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLabel, QFrame, QTableWidget, QTableWidgetItem, QHBoxLayout,
    QPushButton, QSizePolicy
)
from views.utils_view.view_position import center_on_screen
from views.base_window import  BaseWindow
from views.utils_style.styles import GRADIENT_GLOBAL
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor
from PySide6.QtCore import Qt, QSize

# DashboardApp principal
class DashboardApp(BaseWindow):
    def __init__(self):
        super().__init__("SAFET - DashBoard")



        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.setStyleSheet(GRADIENT_GLOBAL)

        # Layout Principal: Horizontal (Sidebar | Contenido)
        self.main_h_layout = QVBoxLayout(main_widget)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_h_layout.setSpacing(0)

        # Header
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: transparent;")
        layout_sidebar = QHBoxLayout(sidebar)
        layout_sidebar.setContentsMargins(0,0,0,0)
        layout_sidebar.setSpacing(0)
        # Logo
        box_logo = QFrame()
        box_logo.setStyleSheet("background-color: transparent;")
        word_logo = QLabel("SATEF")
        word_logo.setObjectName("word_logo")
        layout_logo = QHBoxLayout(box_logo)
        word_logo.setStyleSheet("""
                QLabel#word_logo {
                    color: white;
                    font-size: 30px;
                    font-weight: bold;
                    font-family: sans-serif;
                }
                """)

        layout_logo.setAlignment(Qt.AlignCenter)
        layout_logo.addWidget(word_logo)


        # Titulo
        box_title = QFrame()
        box_title.setStyleSheet("background-color: transparent;")
        word_title = QLabel("Panel de control")
        font_title = QFont("Roboto", 20, QFont.Bold)
        word_title.setFont(font_title)
        layout_title = QHBoxLayout(box_title)
        word_title.setStyleSheet("color: white;")
        layout_title.setAlignment(Qt.AlignCenter)
        layout_title.addWidget(word_title)

        # Profile
        box_profile = QFrame()
        box_profile.setStyleSheet("background-color: transparent;")
        word_profile = QLabel("Admin: Rodrigo .F")
        font_profile = QFont("Roboto", 16, QFont.Bold)
        word_profile.setFont(font_profile)
        layout_profile = QHBoxLayout(box_profile)
        word_profile.setStyleSheet("color: white;")
        layout_profile.setAlignment(Qt.AlignCenter)
        layout_profile.addWidget(word_profile)


        layout_sidebar.addWidget(box_logo,2)
        layout_sidebar.addWidget(box_title,6)
        layout_sidebar.addWidget(box_profile, 2)








        content = QFrame()
        content.setStyleSheet("background-color: transparent; border-top: 1px solid #b3b5b9;")


        self.main_h_layout.addWidget(sidebar, 1)
        self.main_h_layout.addWidget(content, 9)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windos_dashboard = DashboardApp()
    windos_dashboard.show()
    sys.exit(app.exec())




