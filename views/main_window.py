import os
import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLabel, QFrame, QTableWidget, QTableWidgetItem, QHBoxLayout,
    QPushButton, QSizePolicy, QScrollArea
)
from views.utils_view.view_position import center_on_screen
from views.base_window import  BaseWindow
from views.utils_style.styles import GRADIENT_GLOBAL
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve


# DashboardApp principal
class DashboardApp(BaseWindow):
    def __init__(self):
        super().__init__("SAFET - DashBoard")


        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.setStyleSheet(GRADIENT_GLOBAL)

        # 1. Variables de Estado collapse
        self.is_expanded = False
        self.width_collapsed = 50
        self.width_expanded = 250

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
        sidebar.setMaximumHeight(60)

        # Logo
        box_logo = QFrame()
        box_logo.setStyleSheet("background-color: transparent;")
        box_logo.setMaximumWidth( 250)
        word_logo = QLabel("SATEF")
        word_logo.setObjectName("word_logo")
        layout_logo = QHBoxLayout(box_logo)
        layout_logo.setContentsMargins(10,0,0,0)
        word_logo.setStyleSheet("""
                QLabel#word_logo {
                    color: white;
                    font-size: 30px;
                    font-weight: bold;
                    font-family: sans-serif;
                }
                """)

        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setObjectName("toggle_btn")
        self.toggle_btn.setStyleSheet("""
        QPushButton#toggle_btn {
            color: white;
            border: 1px solid white;
            border-radius: 5px;
            font-size: 15px;
            background-color: transparent;
        }
        QPushButton#toggle_btn:hover {
            background-color: #9198a1;
        }
        """)
        self.toggle_btn.clicked.connect(self.toggle_panel)
        self.toggle_btn.setFixedSize(30, 30)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_logo.addWidget(word_logo,9)
        layout_logo.addWidget(self.toggle_btn,1)



        # Titulo
        box_title = QFrame()
        box_title.setStyleSheet("background-color: transparent;")
        word_title = QLabel("Panel de control")
        font_title = QFont("Roboto", 20, QFont.Weight.Bold)
        word_title.setFont(font_title)
        layout_title = QHBoxLayout(box_title)
        word_title.setStyleSheet("color: white;")
        layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_title.addWidget(word_title)

        # Profile
        box_profile = QFrame()
        box_profile.setStyleSheet("background-color: transparent;")
        word_profile = QLabel("Admin: Rodrigo .F")
        font_profile = QFont("Roboto", 16, QFont.Weight.Bold)
        word_profile.setFont(font_profile)
        layout_profile = QHBoxLayout(box_profile)
        word_profile.setStyleSheet("color: white;")
        layout_profile.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_profile.addWidget(word_profile)


        layout_sidebar.addWidget(box_logo,2)
        layout_sidebar.addWidget(box_title,6)
        layout_sidebar.addWidget(box_profile, 2)


        # Content
        content = QFrame()
        content.setStyleSheet("background-color: transparent; border-top: 1px solid #b3b5b9;")
        layout_content = QHBoxLayout(content)
        layout_content.setContentsMargins(0,0,0,0)
        layout_content.setSpacing(0)

        self.content_nav = QFrame()
        self.content_nav.setStyleSheet("background-color: transparent ; border-right: 1px solid #b3b5b9;")
        self.content_nav.setMinimumWidth(self.width_collapsed)
        content_layout = QVBoxLayout(self.content_nav)
        content_layout.setContentsMargins(0,0,0,0)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(3)


        btn_home = QPushButton("Inicio 🏠")
        btn_home.setObjectName("btn_home_1")
        btn_home.setProperty("full_text", "Inicio 🏠")  # Guarda el texto completo para referencia
        btn_home.setProperty("nav_index", 1)  # Guarda el índice de la página
        btn_home.setProperty("is_parent", True)
        btn_home.setFixedHeight(45)
        btn_home.setFont(QFont("Roboto", 12))
        btn_home.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_home.setStyleSheet(
            """
            QPushButton#btn_home_1 {
                color: white; 
                background-color: transparent;
                border: none;
                text-align: center;
                padding-left: 10px;
            }
            QPushButton#btn_home_1:hover {
                background-color:#151a21;
            }
             """
        )
        content_layout.addWidget(btn_home)










        content_view = QFrame()
        content_view.setStyleSheet("background-color: transparent;")







        layout_content.addWidget(self.content_nav,0)
        layout_content.addWidget(content_view, 1)

        self.main_h_layout.addWidget(sidebar, 0)
        self.main_h_layout.addWidget(content, 1)

        # >>> 2. AÑADIDO: CONFIGURACIÓN DEL ANIMADOR <<<
        self.animation = QPropertyAnimation(self.content_nav, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.finished.connect(self.update_state)



    def toggle_panel(self):
        # 1. Determinar el inicio y el fin de la animación basado en el estado
        if self.is_expanded:
            # Colapsar
            start_width = self.width_expanded
            end_width = self.width_collapsed
            self.toggle_btn.setText("☰")  # Cambia el icono a "Menú"
        else:
            # Expandir
            start_width = self.width_collapsed
            end_width = self.width_expanded
            self.toggle_btn.setText("←")  # Cambia el icono a "Flecha"

        self.animation.setStartValue(start_width)
        self.animation.setEndValue(end_width)

        self.animation.start()


    def update_state(self):
        # Invierte el estado SÓLO cuando la animación ha terminado
        self.is_expanded = not self.is_expanded

    def create_nav_button(self, param, param1, param2):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windos_dashboard = DashboardApp()
    windos_dashboard.show()
    sys.exit(app.exec())




