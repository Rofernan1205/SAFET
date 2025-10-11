from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QStackedWidget, QFrame, QLabel, QHBoxLayout
)


class NavButton(QPushButton):
    # Estilos definidos
    NAV_BUTTON_BASE = """
        QPushButton { color: white; background-color: transparent; border: 2px solid green; text-align: left; padding-left: 10px; }
        QPushButton:hover { background-color:#151a21; }
    """
    NAV_BUTTON_ACTIVE = """
        QPushButton { background-color: #151a21; color: white; border: none; text-align: left; padding-left: 10px; }
    """

    def __init__(self, text: str, nav_index: int, is_parent: bool, parent=None):
        # 1. Llama al constructor base
        super().__init__(text, parent)

        # 2. Guarda los metadatos de navegación
        self.nav_index = nav_index
        self.is_parent = is_parent
        self.base_text = text  # Guarda el texto original para poder restaurarlo

        self.setFixedHeight(40)
        self.setFont(QFont("Roboto", 14))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # 3. Estilo inicial (inactivo por defecto)
        self.setStyleSheet(self.NAV_BUTTON_BASE)

        # Si es padre, le damos la flecha inicial de "colapsado"
        if self.is_parent:
            self.setText(f"{self.base_text} ►")

    def activate(self):
        """Aplica el estilo activo y ajusta el texto si es padre (expande)."""
        self.setStyleSheet(self.NAV_BUTTON_ACTIVE)
        if self.is_parent:
            # Cambia la flecha de 'colapsado' a 'expandido'
            self.setText(f"{self.base_text} ▼")

    def deactivate(self):
        """Aplica el estilo inactivo y ajusta el texto si es padre (colapsa)."""
        self.setStyleSheet(self.NAV_BUTTON_BASE)
        if self.is_parent:
            # Vuelve a la flecha de 'colapsado'
            self.setText(f"{self.base_text} ►")


# VISTAS (PÁGINAS) DEL STACKED WIDGET

class HomeView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #2ecc71; border: none;")
        layout = QVBoxLayout(self)
        label = QLabel("Vista de Inicio (Home) - Index 0")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


class ReportsView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Usamos un color diferente para que el cambio sea visible
        self.setStyleSheet("background-color: #3498db; border: none;")
        layout = QVBoxLayout(self)
        label = QLabel("Vista de Reportes - Index 1")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


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

        # Para rastrear el botón que está activo actualmente
        self.active_button = None

        # ---------------------
        # 1. Configuración de Navegación (Izquierda)
        # ---------------------
        self.nav = QFrame(main_widget)  # Parent correcto
        self.nav.setStyleSheet("background-color: #313a45;")
        nav_layout = QVBoxLayout(self.nav)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Botón 1 (Home - Índice 0)
        # Lo configuramos como is_parent=True aunque todavía no tenga lógica de submenú
        self.boton1 = NavButton("Boton 1 (Home)", 0, True, self.nav)
        self.boton1.clicked.connect(lambda: self.set_active_state(self.boton1))
        nav_layout.addWidget(self.boton1)

        # Botón 2 (Reportes - Índice 1)
        self.boton2 = NavButton("Boton 2 (Reportes)", 1, False, self.nav)
        self.boton2.clicked.connect(lambda: self.set_active_state(self.boton2))
        nav_layout.addWidget(self.boton2)

        # ---------------------
        # 2. Configuración de Contenido (Derecha)
        # ---------------------
        self.content = QFrame(main_widget)
        self.content.setStyleSheet("background-color: #34495e;")
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: transparent;")

        # AÑADIR VISTAS (Importante: el orden es el índice)
        self.stacked_widget.addWidget(HomeView())  # Index 0
        self.stacked_widget.addWidget(ReportsView())  # Index 1

        content_layout.addWidget(self.stacked_widget)

        # Añadir al layout principal
        self.main_h_layout.addWidget(self.nav, 1)
        self.main_h_layout.addWidget(self.content, 9)

        # Establecer estado inicial al iniciar la ventana
        self.set_active_state(self.boton1)

    def set_active_state(self, button_to_activate: NavButton):
        """
        Función centralizada que gestiona el estado de los botones y cambia la vista.
        """

        # 1. Desactivar el botón anterior
        if self.active_button and self.active_button != button_to_activate:
            # Si hay un botón activo y no es el mismo que se acaba de clicar, lo desactivamos.
            self.active_button.deactivate()

        # 2. Activar el nuevo botón y actualizar el tracker
        button_to_activate.activate()
        self.active_button = button_to_activate

        # 3. Cambiar la vista en el QStackedWidget
        self.stacked_widget.setCurrentIndex(button_to_activate.nav_index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PruebaVentana()
    window.show()
    sys.exit(app.exec())
