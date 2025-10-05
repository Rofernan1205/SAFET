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

        # 1. Variables de Estado collapse menu
        self.is_expanded = False
        self.width_collapsed = 50
        self.width_expanded = 250

        # 2. Variables de estado de collapse submenu
        self.is_expanded_sub = False
        self.height_collapsed = 0


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
        content_layout.setSpacing(0)



        self.btn_home = QPushButton("🏠 Inicio ")
        self.btn_home.setObjectName("btn_home_1")
        self.btn_home.setProperty("full_text", "🏠 Inicio")  # Guarda el texto completo para referencia
        self.btn_home.setProperty("nav_index", -1)  # Guarda el índice de la página
        self.btn_home.setProperty("is_parent", True)
        self.btn_home.setFixedHeight(40)
        self.btn_home.setFont(QFont("Roboto", 14))
        self.btn_home.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_home.clicked.connect(self.toggle_submenu)

        self.btn_home.setStyleSheet(
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
        content_layout.addWidget(self.btn_home)

        # Area de submenu
        self.submenu_container = QFrame()
        # Inicialmente cerrado
        self.submenu_container.setMaximumHeight(self.height_collapsed)
        self.submenu_container.setStyleSheet("background-color: #3e5a75; border-left: 5px solid red;")
        submenu_layout = QVBoxLayout(self.submenu_container)
        submenu_layout.setContentsMargins(0, 0, 0, 0)
        submenu_layout.setSpacing(0)

        self.btn_sub_1 = QPushButton("Botton 1")
        self.btn_sub_1.setFont(QFont("Roboto", 14))
        self.btn_sub_1.setStyleSheet("color:white; background-color : green;padding: 5")
        self.btn_sub_2 = QPushButton("Botton 2")
        self.btn_sub_2.setFont(QFont("Roboto", 14))
        self.btn_sub_2.setStyleSheet("color:white; background-color : blue; padding: 5")
        submenu_layout.addWidget(self.btn_sub_1)
        submenu_layout.addWidget(self.btn_sub_2)
        content_layout.addWidget(self.submenu_container)




        content_view = QFrame()
        content_view.setStyleSheet("background-color: transparent;")


        layout_content.addWidget(self.content_nav,0)
        layout_content.addWidget(content_view, 1)

        self.main_h_layout.addWidget(sidebar, 0)
        self.main_h_layout.addWidget(content, 1)

        # >>> 1. ANIMACIÓN DE COLLPASE MENU
        self.animation_menu = QPropertyAnimation(self.content_nav, b"minimumWidth")
        self.animation_menu.setDuration(300)
        self.animation_menu.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation_menu.finished.connect(self.update_state_menu)

        # >>> 2 ANIMACIÓN DE COLLAPSE SUBMENU

        self.animation_submenu = QPropertyAnimation(self.submenu_container,b"maximumHeight")
        self.animation_menu.setDuration(300)
        self.animation_submenu.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation_submenu.finished.connect(self.update_state_submenu)




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

        self.animation_menu.setStartValue(start_width)
        self.animation_menu.setEndValue(end_width)
        self.animation_menu.start()


    def update_state_menu(self):
        self.is_expanded = not self.is_expanded

    def toggle_submenu(self):
        target_layout = self.submenu_container .layout()
        required_height = 0

        if target_layout:
            for i in range(target_layout.count()):
                item = target_layout.itemAt(i)
                widget = item.widget()
                if widget:
                    required_height += widget.sizeHint().height()

            spacing = target_layout.spacing()
            required_height += spacing * (target_layout.count() - 1)

        if self.is_expanded_sub:
            start_height = required_height
            end_height = self.height_collapsed
            self.btn_home.setStyleSheet(
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
                
            }""")

        else:
            start_height = self.height_collapsed
            end_height = required_height
            self.btn_home.setStyleSheet(
                """
                QPushButton#btn_home_1 {
                background-color: #151a21;
                color: white; 
                border: none;
                text-align: center;
                padding-left: 10px;
                }""")

        self.animation_submenu.setStartValue(start_height)
        self.animation_submenu.setEndValue(end_height)
        self.animation_submenu.start()



    def update_state_submenu(self):
        self.is_expanded_sub = not self.is_expanded_sub




if __name__ == "__main__":
    app = QApplication(sys.argv)
    windos_dashboard = DashboardApp()
    windos_dashboard.show()
    sys.exit(app.exec())




