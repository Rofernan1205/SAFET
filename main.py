import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QFrame, QHBoxLayout, QPushButton, QStackedWidget,
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve


# =====================================================================
# SIMULACIÓN DE CLASES Y ESTILOS EXTERNOS
# =====================================================================

class BaseWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(800, 600)


def center_on_screen(widget):
    screen = QApplication.primaryScreen().geometry()
    x = (screen.width() - widget.width()) // 2
    y = (screen.height() - widget.height()) // 2
    widget.setGeometry(x, y, widget.width(), widget.height())


GRADIENT_GLOBAL = """
    QWidget {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #2c3e50, stop:1 #34495e); /* Azul oscuro / Gris oscuro */
    }
"""


# =====================================================================
# CLASES DE VISTA DE CONTENIDO (PLACEHOLDERS)
# =====================================================================

# Vistas de ejemplo (mantienen sus índices: 0, 1, 2, 3, 4)
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
        self.setStyleSheet("background-color: #3498db; border: none;")
        layout = QVBoxLayout(self)
        label = QLabel("Vista de Reportes - Index 1")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


class Sub1View(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #f1c40f; border: none;")
        layout = QVBoxLayout(self)
        label = QLabel("Vista de Submenú 1 - Index 2")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


class Sub2View(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #e74c3c; border: none;")
        layout = QVBoxLayout(self)
        label = QLabel("Vista de Submenú 2 - Index 3")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


class Sub3View(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #9b59b6; border: none;")
        layout = QVBoxLayout(self)
        label = QLabel("Vista de Submenú 3 - Index 4")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


# =====================================================================
# CLASE REUTILIZABLE PARA BOTONES DE NAVEGACIÓN
# (Estilos simplificados)
# =====================================================================

class MenuButton(QPushButton):
    """Botón principal de menú (Padres)."""
    NAV_BUTTON_BASE_STYLE = """
        QPushButton { color: white; background-color: transparent; border: none; text-align: left; padding-left: 10px; }
        QPushButton:hover { background-color:#151a21; }
    """
    NAV_BUTTON_ACTIVE_STYLE = """
        QPushButton { background-color: #151a21; color: white; border: none; text-align: left; padding-left: 10px; }
    """

    def __init__(self, text, object_name=None, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setFont(QFont("Roboto", 14))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self.NAV_BUTTON_BASE_STYLE)
        if object_name: self.setObjectName(object_name)


class SubMenuButton(QPushButton):
    """Botón de submenú (Hijos)."""
    SUB_BUTTON_BASE_STYLE = "color:white; background-color : transparent; padding: 5; text-align: left; padding-left: 20px;"
    SUB_BUTTON_ACTIVE_STYLE = "color:white; background-color : #151a21; padding: 5; text-align: left; padding-left: 20px;"

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setFont(QFont("Roboto", 14))
        self.setStyleSheet(self.SUB_BUTTON_BASE_STYLE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class DashboardApp(BaseWindow):
    # Textos del botón Home para indicar estado
    HOME_TEXT_COLLAPSED = "🏠 Inicio ►"
    HOME_TEXT_EXPANDED = "🏠 Inicio ▼"
    HOME_TEXT_BASE = "🏠 Inicio "

    def __init__(self):
        super().__init__("SAFET - DashBoard")
        self._define_constants()

        # Variable para rastrear el botón actualmente activo
        self.active_button = None

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.setStyleSheet(GRADIENT_GLOBAL)

        self.main_h_layout = QVBoxLayout(main_widget)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_h_layout.setSpacing(0)

        self._setup_header()
        self._setup_navigation(main_widget)
        self._setup_animations()

        # Establecer la vista inicial y el botón activo (Home, Index 0)
        self._set_active_state(self.btn_home, 0)
        self.btn_home.setText(self.HOME_TEXT_BASE)  # Se asegura que inicie sin flecha activa

    def _define_constants(self):
        # Variables de Estado collapse menu
        self.is_expanded = False
        self.width_collapsed = 50
        self.width_expanded = 250

        # Variables de estado de collapse submenu
        self.is_expanded_sub = False
        self.height_collapsed = 0

    def _setup_header(self):
        """Configura la barra superior (Header)."""
        # (El código del header se mantiene igual)
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: transparent;")
        layout_sidebar = QHBoxLayout(sidebar)
        layout_sidebar.setContentsMargins(0, 0, 0, 0)
        layout_sidebar.setSpacing(0)
        sidebar.setMaximumHeight(60)

        # --- Logo Box ---
        box_logo = QFrame()
        box_logo.setStyleSheet("background-color: transparent;")
        box_logo.setMaximumWidth(self.width_expanded)
        word_logo = QLabel("SATEF")
        word_logo.setObjectName("word_logo")
        word_logo.setStyleSheet(
            "QLabel#word_logo {color: white; font-size: 30px; font-weight: bold; font-family: sans-serif;}")

        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setObjectName("toggle_btn")
        self.toggle_btn.setStyleSheet("""
        QPushButton#toggle_btn {
            color: white; border: 1px solid white; border-radius: 5px;
            font-size: 15px; background-color: transparent;
        }
        QPushButton#toggle_btn:hover { background-color: #9198a1; }
        """)
        self.toggle_btn.clicked.connect(self.toggle_panel)
        self.toggle_btn.setFixedSize(30, 30)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout_logo = QHBoxLayout(box_logo)
        layout_logo.setContentsMargins(10, 0, 0, 0)
        layout_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_logo.addWidget(word_logo, 9)
        layout_logo.addWidget(self.toggle_btn, 1)

        # --- Title Box ---
        box_title = QFrame()
        box_title.setStyleSheet("background-color: transparent;")
        word_title = QLabel("Panel de control")
        word_title.setFont(QFont("Roboto", 20, QFont.Weight.Bold))
        word_title.setStyleSheet("color: white;")

        layout_title = QHBoxLayout(box_title)
        layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_title.addWidget(word_title)

        # --- Profile Box ---
        box_profile = QFrame()
        box_profile.setStyleSheet("background-color: transparent;")
        word_profile = QLabel("Admin: Rodrigo .F")
        word_profile.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
        word_profile.setStyleSheet("color: white;")

        layout_profile = QHBoxLayout(box_profile)
        layout_profile.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_profile.addWidget(word_profile)

        # Añadir al Layout del Header
        layout_sidebar.addWidget(box_logo, 2)
        layout_sidebar.addWidget(box_title, 6)
        layout_sidebar.addWidget(box_profile, 2)

        self.main_h_layout.addWidget(sidebar, 0)

    def _setup_navigation(self, main_widget):
        """Configura el área de contenido principal y la navegación lateral."""

        content = QFrame()
        content.setStyleSheet("background-color: transparent; border-top: 1px solid #b3b5b9;")
        layout_content = QHBoxLayout(content)
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_content.setSpacing(0)

        self.content_nav = QFrame()
        self.content_nav.setStyleSheet("background-color: transparent ; border-right: 1px solid #b3b5b9;")
        self.content_nav.setMinimumWidth(self.width_collapsed)
        content_layout = QVBoxLayout(self.content_nav)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(0)

        # ===============================================
        # CONFIGURACIÓN DE VISTAS (StackedWidget)
        # ===============================================
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: transparent;")

        self.stacked_widget.addWidget(HomeView())  # Index 0
        self.stacked_widget.addWidget(ReportsView())  # Index 1
        self.stacked_widget.addWidget(Sub1View())  # Index 2
        self.stacked_widget.addWidget(Sub2View())  # Index 3
        self.stacked_widget.addWidget(Sub3View())  # Index 4

        # ===============================================
        # CONFIGURACIÓN Y CONEXIONES DE BOTONES
        # ===============================================

        # Botón principal (Home) - Index 0. Conectado a la función de ANIMACIÓN/TOGGLE
        self.btn_home = MenuButton(self.HOME_TEXT_COLLAPSED, object_name="btn_home_1")
        self.btn_home.clicked.connect(self.toggle_submenu)
        content_layout.addWidget(self.btn_home)

        # Área de submenu
        self.submenu_container = QFrame()
        self.submenu_container.setMaximumHeight(self.height_collapsed)
        self.submenu_container.setStyleSheet("background-color: #3e5a75; border-left: 5px solid red;")
        submenu_layout = QVBoxLayout(self.submenu_container)
        submenu_layout.setContentsMargins(0, 0, 0, 0)
        submenu_layout.setSpacing(0)

        # Botones del Submenú (Hijos). Conectados a la función CENTRALIZADA.
        self.btn_sub_1 = SubMenuButton("▷ Submenú 1")
        self.btn_sub_2 = SubMenuButton("▷ Submenú 2")
        self.btn_sub_3 = SubMenuButton("▷ Submenú 3 - Nuevo")

        # Uso de la función CENTRALIZADA para manejar estilo y vista
        self.btn_sub_1.clicked.connect(lambda: self._set_active_state(self.btn_sub_1, 2))
        self.btn_sub_2.clicked.connect(lambda: self._set_active_state(self.btn_sub_2, 3))
        self.btn_sub_3.clicked.connect(lambda: self._set_active_state(self.btn_sub_3, 4))

        submenu_layout.addWidget(self.btn_sub_1)
        submenu_layout.addWidget(self.btn_sub_2)
        submenu_layout.addWidget(self.btn_sub_3)

        content_layout.addWidget(self.submenu_container)

        # Botón Reportes - Index 1. Conectado a la función CENTRALIZADA.
        self.btn_reports = MenuButton("📊 Reportes")
        self.btn_reports.clicked.connect(lambda: self._set_active_state(self.btn_reports, 1))
        content_layout.addWidget(self.btn_reports)

        # Contenido de la vista principal
        layout_content.addWidget(self.content_nav, 0)
        layout_content.addWidget(self.stacked_widget, 1)

        self.main_h_layout.addWidget(content, 1)

    def _setup_animations(self):
        """Configura los objetos QPropertyAnimation."""
        self.animation_menu = QPropertyAnimation(self.content_nav, b"minimumWidth")
        self.animation_menu.setDuration(300)
        self.animation_menu.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation_menu.finished.connect(self.update_state_menu)

        self.animation_submenu = QPropertyAnimation(self.submenu_container, b"maximumHeight")
        self.animation_submenu.setDuration(300)
        self.animation_submenu.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation_submenu.finished.connect(self.update_state_submenu)

    def toggle_panel(self):
        """Alterna la expansión/colapso del menú principal lateral."""
        if self.is_expanded:
            start_width, end_width = self.width_expanded, self.width_collapsed
            self.toggle_btn.setText("☰")
        else:
            start_width, end_width = self.width_collapsed, self.width_expanded
            self.toggle_btn.setText("←")

        self.animation_menu.setStartValue(start_width)
        self.animation_menu.setEndValue(end_width)
        self.animation_menu.start()

    def update_state_menu(self):
        self.is_expanded = not self.is_expanded

    def _calculate_submenu_height(self):
        """Calcula la altura total necesaria para el submenú."""
        target_layout = self.submenu_container.layout()
        required_height = 0
        if target_layout:
            for i in range(target_layout.count()):
                item = target_layout.itemAt(i)
                widget = item.widget()
                if widget:
                    required_height += widget.sizeHint().height()
            required_height += target_layout.spacing() * (target_layout.count() - 1)
        return required_height

    def _collapse_submenu(self):
        """Ejecuta la animación de colapso y actualiza el estado."""
        required_height = self._calculate_submenu_height()
        self.animation_submenu.setStartValue(required_height)
        self.animation_submenu.setEndValue(self.height_collapsed)
        self.animation_submenu.start()
        self.is_expanded_sub = False
        self.btn_home.setText(self.HOME_TEXT_COLLAPSED)  # Flecha ►

    def toggle_submenu(self):
        """Maneja la lógica de animación de expansión/colapso para el submenú del Home."""
        required_height = self._calculate_submenu_height()

        if self.is_expanded_sub:
            # CERRAR
            self._collapse_submenu()

            # Al cerrar, si el botón activo era un hijo, lo desactivamos y volvemos a activar Home.
            if self.active_button in [self.btn_sub_1, self.btn_sub_2, self.btn_sub_3]:
                # Usamos _set_active_state para limpiar el estilo del hijo y aplicar estilo activo al padre.
                self._set_active_state(self.btn_home, self.stacked_widget.currentIndex())
                self.btn_home.setText(self.HOME_TEXT_COLLAPSED)  # La flecha se cierra inmediatamente después.

        else:
            # ABRIR
            self.animation_submenu.setStartValue(self.height_collapsed)
            self.animation_submenu.setEndValue(required_height)
            self.animation_submenu.start()
            self.is_expanded_sub = True

            # Usamos la función CENTRALIZADA para manejar el estilo y el contenido (Index 0)
            self._set_active_state(self.btn_home, 0)
            self.btn_home.setText(self.HOME_TEXT_EXPANDED)  # Flecha ▼

    def update_state_submenu(self):
        pass

    def _set_active_state(self, button_to_activate, index):
        """
        [FUNCIÓN CENTRALIZADA]
        Cambia la vista y actualiza el estilo de activación de CUALQUIER botón
        (padre, hijo o botón principal simple).

        :param button_to_activate: El botón que debe ser marcado como activo.
        :param index: El índice de la vista a mostrar.
        """

        # 1. No hacer nada si ya está activo
        if self.active_button == button_to_activate:
            return

        # 2. Desactivar el botón anterior
        if self.active_button:
            if isinstance(self.active_button, MenuButton):
                self.active_button.setStyleSheet(MenuButton.NAV_BUTTON_BASE_STYLE)
            elif isinstance(self.active_button, SubMenuButton):
                self.active_button.setStyleSheet(SubMenuButton.SUB_BUTTON_BASE_STYLE)

            # Si el botón anterior no era el Home, resetear el texto del Home.
            if self.active_button != self.btn_home:
                self.btn_home.setText(self.HOME_TEXT_BASE)

            # Si el nuevo botón no es parte del submenú de Home (es Reports), cerramos el submenú.
            if button_to_activate not in [self.btn_home, self.btn_sub_1, self.btn_sub_2,
                                          self.btn_sub_3] and self.is_expanded_sub:
                self._collapse_submenu()  # Cierra el submenú con animación

        # 3. Activar el nuevo botón y ajustar estados
        if isinstance(button_to_activate, MenuButton):
            # Es un botón de menú principal (Home o Reports)
            button_to_activate.setStyleSheet(MenuButton.NAV_BUTTON_ACTIVE_STYLE)

            # Si es Reports, asegurarse de que Home no muestre ninguna flecha activa
            if button_to_activate == self.btn_reports:
                self.btn_home.setText(self.HOME_TEXT_BASE)

        elif isinstance(button_to_activate, SubMenuButton):
            # Es un botón de submenú (Hijo)
            button_to_activate.setStyleSheet(SubMenuButton.SUB_BUTTON_ACTIVE_STYLE)

            # Asegurarse de que el padre (btn_home) se mantenga visualmente activo y expandido
            self.btn_home.setStyleSheet(MenuButton.NAV_BUTTON_ACTIVE_STYLE)
            self.btn_home.setText(self.HOME_TEXT_EXPANDED)

            # Si el submenú estaba cerrado, lo abrimos automáticamente
            if not self.is_expanded_sub:
                self.toggle_submenu()

        self.active_button = button_to_activate

        # 4. Cambiar la vista
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windos_dashboard = DashboardApp()
    windos_dashboard.show()
    sys.exit(app.exec())
