from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QStackedWidget, QFrame, QLabel, QHBoxLayout
)


class NavButton(QPushButton):
    NAV_BUTTON_BASE = """
        QPushButton { color: white; background-color: transparent; border:none; text-align: center; padding-left: 10px; }
        QPushButton:hover { background-color:#333a45 ; }
    """
    NAV_BUTTON_ACTIVE = """
        QPushButton { background-color: #333a45; color: white; border: none; text-align: center; padding-left: 10px; }
    """
    # Usaremos estos estilos en el futuro para los sub-botones, por ahora se mantienen simples
    SUB_BUTTON_BASE = "color:white; background-color : transparent; padding: 5; text-align: left; padding-left: 20px;"
    SUB_BUTTON_ACTIVE = "color:white; background-color : #151a21; padding: 5; text-align: left; padding-left: 20px;"

    def __init__(self, text: str, nav_index: int, is_parent: bool, parent=None):

        super().__init__(text, parent)

        self.nav_index = nav_index
        self.is_parent = is_parent
        self.base_text = text

        self.setFixedHeight(40)
        self.setFont(QFont("Roboto", 14))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet(self.NAV_BUTTON_BASE)

        # Si es padre, le damos la flecha inicial de "colapsado"
        if self.is_parent:
            self.setText(f"{self.base_text} ►")

    def activate(self):
        """Aplica el estilo activo (encendido)."""
        self.setStyleSheet(self.NAV_BUTTON_ACTIVE)
        if self.is_parent:
            # Cambia la flecha de 'colapsado' a 'expandido'
            self.setText(f"{self.base_text} ▼")

    def deactivate(self):
        """Aplica el estilo inactivo (apagado)."""
        self.setStyleSheet(self.NAV_BUTTON_BASE)
        if self.is_parent:
            # Vuelve a la flecha de 'colapsado'
            self.setText(f"{self.base_text} ►")


# VISTAS (PÁGINAS) DEL STACKED WIDGET

class BaseView(QFrame):
    """Clase base para simplificar la creación de vistas."""

    def __init__(self, text, index, color, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {color}; border: none;")
        layout = QVBoxLayout(self)
        label = QLabel(f"Vista de {text} - Index {index}")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


class HomeView(BaseView):
    def __init__(self, parent=None): super().__init__("Inicio (Home)", 0, "#2ecc71", parent)


class ReportsView(BaseView):
    def __init__(self, parent=None): super().__init__("Reportes", 1, "#3498db", parent)


class SettingsView(BaseView):
    def __init__(self, parent=None): super().__init__("Configuración", 2, "#f1c40f", parent)


class PruebaVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana de prueba")
        self.setMinimumSize(960, 540)
        self.resize(1280, 720)

        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: #202020;")
        self.setCentralWidget(main_widget)

        self.main_h_layout = QHBoxLayout(main_widget)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_h_layout.setSpacing(0)

        # CLAVE: active_button almacena el objeto NavButton (NO el índice)
        self.active_button = None

        # ---------------------
        # 1. Configuración de Navegación (Izquierda)
        # ---------------------
        self.nav = QFrame(main_widget)
        self.nav.setStyleSheet("background-color: #313a45;")
        nav_layout = QVBoxLayout(self.nav)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Botón 1 (Home - Índice 0)
        self.boton1 = NavButton("Boton 1 (Home)", 0, True, self.nav)
        self.boton1.clicked.connect(lambda: self.set_active_state(self.boton1))
        nav_layout.addWidget(self.boton1)

        # Botón 2 (Reportes - Índice 1)
        self.boton2 = NavButton("Boton 2 (Reportes)", 1, False, self.nav)
        self.boton2.clicked.connect(lambda: self.set_active_state(self.boton2))
        nav_layout.addWidget(self.boton2)

        # Botón 3 (Configuración - Índice 2)
        self.boton3 = NavButton("Boton 3 (Config)", 2, False, self.nav)
        self.boton3.clicked.connect(lambda: self.set_active_state(self.boton3))
        nav_layout.addWidget(self.boton3)

        # ---------------------
        # 2. Configuración de Contenido (Derecha)
        # ---------------------
        self.content = QFrame(main_widget)
        self.content.setStyleSheet("background-color: #34495e;")
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: transparent;")

        # AÑADIR VISTAS
        self.stacked_widget.addWidget(HomeView())  # Index 0
        self.stacked_widget.addWidget(ReportsView())  # Index 1
        self.stacked_widget.addWidget(SettingsView())  # Index 2

        content_layout.addWidget(self.stacked_widget)

        # Añadir al layout principal
        self.main_h_layout.addWidget(self.nav, 1)
        self.main_h_layout.addWidget(self.content, 9)

        # Establecer estado inicial al iniciar la ventana
        self.set_active_state(self.boton1)

    def set_active_state(self, button_to_activate: NavButton):
        if self.active_button and self.active_button is not button_to_activate:
            self.active_button.deactivate()
        self.stacked_widget.setCurrentIndex(button_to_activate.nav_index)
        button_to_activate.activate()
        self.active_button = button_to_activate
        print(self.active_button)




