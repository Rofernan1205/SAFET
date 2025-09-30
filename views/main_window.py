import os
import sys
from email.header import Header

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

        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: transparent;")
        layout_sidebar = QHBoxLayout(sidebar)
        layout_sidebar.setContentsMargins(0,0,0,0)
        layout_sidebar.setSpacing(0)

        box_logo = QFrame()
        box_logo.setStyleSheet("background-color: red;")

        box_title = QFrame()
        box_title.setStyleSheet("background-color: green;")

        box_profile = QFrame()
        box_profile.setStyleSheet("background-color: blue;")


        layout_sidebar.addWidget(box_logo,2)
        layout_sidebar.addWidget(box_title,4)
        layout_sidebar.addWidget(box_profile, 4)








        content = QFrame()
        content.setStyleSheet("background-color: transparent; border-top: 1px solid #b3b5b9;")

        # Sidebar 20% - Content 80%
        self.main_h_layout.addWidget(sidebar, 1)
        self.main_h_layout.addWidget(content, 9)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windos_dashboard = DashboardApp()
    windos_dashboard.show()
    sys.exit(app.exec())



        # box_logo = QFrame()
        # box_logo.setStyleSheet("backbround-color: red;")
        # layout_sidebar.addWidget(box_logo)
        #
        # ruta = os.getcwd()
        # nueva_ruta = ruta[:len(ruta)-6]
        # logo_pixmap = QPixmap(os.path.join(nueva_ruta, r"assets\images\apubyte.jpg"))
        #
        # if logo_pixmap.isNull():
        #     print("¡ERROR! No se pudo cargar la imagen. Revisa la ruta.")
        # else:
        #     print("Imagen cargada exitosamente.")
        #
        # label = QLabel()
        # label.setPixmap(logo_pixmap)
        # label.setScaledContents(True)  # Hace que la imagen se ajuste al tamaño del QLabel
        # label.resize(300, 200)
        # box_logo.addWidget(label)
