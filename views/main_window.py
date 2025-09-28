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
        self.main_h_layout = QHBoxLayout(main_widget)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_h_layout.setSpacing(0)

        header = QWidget()
        header.setStyleSheet("border-bottom: 2px solid white; background-color:red;")

        self.main_h_layout.addWidget(header)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windos_dashboard = DashboardApp()
    windos_dashboard.show()
    sys.exit(app.exec())


