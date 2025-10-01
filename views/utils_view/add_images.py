import os
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QGridLayout


def get_images_path(path_i):
    path = os.getcwd()
    path_f = path[:len(path)-6]
    path_c = os.path.join(path_f, path_i)
    return path_c


# box_logo_layout = QGridLayout(box_logo)
# box_logo_layout.setAlignment(Qt.AlignCenter)
# box_logo.setMinimumHeight(100)  # asegura altura
# logo = QLabel("SAFET")
# logo.setMinimumSize(60, 100)
# logo_path = get_images_path(r"assets\images\safet.png")
# pixmap = QPixmap(logo_path)
# logo.setPixmap(pixmap)
# logo.setScaledContents(True)
# box_logo_layout.addWidget(logo)
