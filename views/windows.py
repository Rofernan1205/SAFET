import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QFrame, QHBoxLayout, QPushButton, QStackedWidget,
)
# from views.utils_view.view_position import center_on_screen
# from views.base_window import BaseWindow
# from views.utils_style.styles import GRADIENT_GLOBAL
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
        # center_on_screen(self) # Se quita el centrado para mantener el código minimalista


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

# =====================================================================
# CLASES DE VISTA DE CONTENIDO (PLACEHOLDERS)
# =====================================================================

class HomeView(QFrame):
    """Vista de ejemplo para la página de Inicio."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #2ecc71; border: none;")  # Verde esmeralda
        layout = QVBoxLayout(self)
        label = QLabel("Vista de Inicio (Home) - Index 0")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


class ReportsView(QFrame):
    """Vista de ejemplo para la página de Reportes."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #3498db; border: none;")  # Azul
        layout = QVBoxLayout(self)
        label = QLabel("Vista de Reportes - Index 1")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


# Nuevas vistas para el submenú
class Sub1View(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #f1c40f; border: none;")  # Amarillo
        layout = QVBoxLayout(self)
        label = QLabel("Vista de Submenú 1 - Index 2")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


class Sub2View(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #e74c3c; border: none;")  # Rojo
        layout = QVBoxLayout(self)
        label = QLabel("Vista de Submenú 2 - Index 3")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


class Sub3View(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #9b59b6; border: none;")  # Púrpura
        layout = QVBoxLayout(self)
        label = QLabel("Vista de Submenú 3 - Index 4")
        label.setFont(QFont("Roboto", 30))
        label.setStyleSheet("color: white;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


# =====================================================================
# CLASE REUTILIZABLE PARA BOTONES DE NAVEGACIÓN
# =====================================================================

class MenuButton(QPushButton):
    """Botón base reutilizable para el menú principal (padre)."""

    NAV_BUTTON_BASE_STYLE = """
        QPushButton {
            color: white; 
            background-color: transparent;
            border: none;
            text-align: left; /* Alineación a la izquierda */
            padding-left: 10px;
        }
        QPushButton:hover {
            background-color:#151a21; /* Fondo más oscuro al pasar el ratón */
        }
    """

    NAV_BUTTON_ACTIVE_STYLE = """
        QPushButton {
            background-color: #151a21; /* Fondo activo/seleccionado */
            color: white; 
            border: none;
            text-align: left;
            padding-left: 10px;
        }
    """

    def __init__(self, text, object_name=None, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setFont(QFont("Roboto", 14))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self.NAV_BUTTON_BASE_STYLE)
        if object_name:
            self.setObjectName(object_name)


class SubMenuButton(QPushButton):
    """Botón base reutilizable para los elementos del submenú."""

    SUB_BUTTON_BASE_STYLE = "color:white; background-color : transparent; padding: 5; text-align: left; padding-left: 20px;"
    SUB_BUTTON_ACTIVE_STYLE = "color:white; background-color : #151a21; padding: 5; text-align: left; padding-left: 20px;"

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)  # CONSISTENCIA: Altura fija
        self.setFont(QFont("Roboto", 14))
        self.setStyleSheet(self.SUB_BUTTON_BASE_STYLE)  # Usar estilo base
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class DashboardApp(BaseWindow):
    # Textos del botón Home para indicar estado
    HOME_TEXT_COLLAPSED = "🏠 Inicio ►"
    HOME_TEXT_EXPANDED = "🏠 Inicio ▼"
    HOME_TEXT_BASE = "🏠 Inicio "  # Para cuando el submenú está cerrado y no es activo

    def __init__(self):
        super().__init__("SAFET - DashBoard")
        self._define_constants()

        # Nueva variable para rastrear el botón actualmente activo
        self.active_button = None

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.setStyleSheet(GRADIENT_GLOBAL)

        # Configuración del Layout Principal
        self.main_h_layout = QVBoxLayout(main_widget)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_h_layout.setSpacing(0)

        self._setup_header()
        self._setup_navigation(main_widget)
        self._setup_animations()

        # Establecer la vista inicial y el botón activo
        self._change_view(self.btn_home, 0)
        # Inicializar el texto del botón home
        self.btn_home.setText(self.HOME_TEXT_BASE)

    def _define_constants(self):
        """Define las variables de estado y tamaño."""
        # 1. Variables de Estado collapse menu
        self.is_expanded = False
        self.width_collapsed = 50
        self.width_expanded = 250

        # 2. Variables de estado de collapse submenu
        self.is_expanded_sub = False
        self.height_collapsed = 0

    # ... (el resto de _setup_header se mantiene sin cambios) ...
    def _setup_header(self):
        """Configura la barra superior (Header) con Logo, Título y Perfil."""
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: transparent;")
        layout_sidebar = QHBoxLayout(sidebar)
        layout_sidebar.setContentsMargins(0, 0, 0, 0)
        layout_sidebar.setSpacing(0)
        sidebar.setMaximumHeight(60)

        # --- Logo Box ---
        box_logo = QFrame()
        box_logo.setStyleSheet("background-color: transparent;")
        box_logo.setMaximumWidth(self.width_expanded)  # Usar la constante de ancho expandido
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

        # Content (Contenedor de Sidebar y View)
        content = QFrame()
        content.setStyleSheet("background-color: transparent; border-top: 1px solid #b3b5b9;")
        layout_content = QHBoxLayout(content)
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_content.setSpacing(0)

        # Navigation Sidebar (Content Nav)
        self.content_nav = QFrame()
        self.content_nav.setStyleSheet("background-color: transparent ; border-right: 1px solid #b3b5b9;")
        self.content_nav.setMinimumWidth(self.width_collapsed)
        content_layout = QVBoxLayout(self.content_nav)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(0)

        # ===============================================
        # CONFIGURACIÓN DE VISTAS (PÁGINAS)
        # ===============================================
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: transparent;")

        self.home_view = HomeView()
        self.reports_view = ReportsView()
        self.sub1_view = Sub1View()
        self.sub2_view = Sub2View()
        self.sub3_view = Sub3View()

        self.stacked_widget.addWidget(self.home_view)  # Index 0: Vista de Inicio (Home)
        self.stacked_widget.addWidget(self.reports_view)  # Index 1: Vista de Reportes
        self.stacked_widget.addWidget(self.sub1_view)  # Index 2: Vista Sub 1
        self.stacked_widget.addWidget(self.sub2_view)  # Index 3: Vista Sub 2
        self.stacked_widget.addWidget(self.sub3_view)  # Index 4: Vista Sub 3

        # ===============================================
        # CONFIGURACIÓN DE BOTONES
        # ===============================================

        # Botón principal (Home) - Index 0
        self.btn_home = MenuButton(self.HOME_TEXT_COLLAPSED, object_name="btn_home_1")
        self.btn_home.setProperty("is_parent", True)
        self.btn_home.clicked.connect(self.toggle_submenu)
        content_layout.addWidget(self.btn_home)

        # Área de submenu
        self.submenu_container = QFrame()
        self.submenu_container.setMaximumHeight(self.height_collapsed)
        self.submenu_container.setStyleSheet("background-color: #3e5a75; border-left: 5px solid red;")
        submenu_layout = QVBoxLayout(self.submenu_container)
        submenu_layout.setContentsMargins(0, 0, 0, 0)
        submenu_layout.setSpacing(0)

        # Botones del Submenú
        self.btn_sub_1 = SubMenuButton("▷ Submenú 1")
        self.btn_sub_2 = SubMenuButton("▷ Submenú 2")
        self.btn_sub_3 = SubMenuButton("▷ Submenú 3 - Nuevo")

        # Conexión de submenús a sus respectivas vistas
        # Usamos MenuButton.NAV_BUTTON_BASE_STYLE para desmarcar el padre (btn_home) si se activa un hijo
        self.btn_sub_1.clicked.connect(lambda: self._change_view(self.btn_sub_1, 2, parent_button=self.btn_home))
        self.btn_sub_2.clicked.connect(lambda: self._change_view(self.btn_sub_2, 3, parent_button=self.btn_home))
        self.btn_sub_3.clicked.connect(lambda: self._change_view(self.btn_sub_3, 4, parent_button=self.btn_home))

        submenu_layout.addWidget(self.btn_sub_1)
        submenu_layout.addWidget(self.btn_sub_2)
        submenu_layout.addWidget(self.btn_sub_3)

        content_layout.addWidget(self.submenu_container)

        # Otro botón de menú (ejemplo de reutilización) - Index 1
        self.btn_reports = MenuButton("📊 Reportes")
        # Conectamos a _change_view, le pasamos el botón a activar y el índice de la vista (1)
        self.btn_reports.clicked.connect(lambda: self._change_view(self.btn_reports, 1))
        content_layout.addWidget(self.btn_reports)

        # Contenido de la vista principal (StackedWidget)
        layout_content.addWidget(self.content_nav, 0)
        layout_content.addWidget(self.stacked_widget, 1)  # <-- Usamos el StackedWidget

        self.main_h_layout.addWidget(content, 1)

    def _setup_animations(self):
        """Configura los objetos QPropertyAnimation."""

        # 1. ANIMACIÓN DE COLLAPSE MENU (Ancho)
        self.animation_menu = QPropertyAnimation(self.content_nav, b"minimumWidth")
        self.animation_menu.setDuration(300)
        self.animation_menu.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation_menu.finished.connect(self.update_state_menu)

        # 2. ANIMACIÓN DE COLLAPSE SUBMENU (Altura)
        self.animation_submenu = QPropertyAnimation(self.submenu_container, b"maximumHeight")
        self.animation_submenu.setDuration(300)
        self.animation_submenu.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation_submenu.finished.connect(self.update_state_submenu)

    def toggle_panel(self):
        # ... (La lógica de toggle_panel se mantiene) ...
        if self.is_expanded:
            start_width = self.width_expanded
            end_width = self.width_collapsed
            self.toggle_btn.setText("☰")
        else:
            start_width = self.width_collapsed
            end_width = self.width_expanded
            self.toggle_btn.setText("←")

        self.animation_menu.setStartValue(start_width)
        self.animation_menu.setEndValue(end_width)
        self.animation_menu.start()

    def update_state_menu(self):
        self.is_expanded = not self.is_expanded

    def toggle_submenu_collapse_only(self):
        """Fuerza el colapso del submenú si está expandido, sin cambiar la vista activa."""
        if self.is_expanded_sub:
            target_layout = self.submenu_container.layout()
            required_height = 0
            if target_layout:
                for i in range(target_layout.count()):
                    item = target_layout.itemAt(i)
                    widget = item.widget()
                    if widget:
                        required_height += widget.sizeHint().height()

            start_height = required_height
            end_height = self.height_collapsed

            self.animation_submenu.setStartValue(start_height)
            self.animation_submenu.setEndValue(end_height)
            self.animation_submenu.start()
            self.is_expanded_sub = False  # Actualizar el estado inmediatamente
            self.btn_home.setText(self.HOME_TEXT_COLLAPSED)  # Cambiar flecha a colapsado

    def toggle_submenu(self):
        target_layout = self.submenu_container.layout()
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
            # CERRAR
            start_height = required_height
            end_height = self.height_collapsed
            self.btn_home.setStyleSheet(MenuButton.NAV_BUTTON_BASE_STYLE)
            self.btn_home.setText(self.HOME_TEXT_COLLAPSED)  # Establecer flecha a colapsado

            # Si se cierra el submenú y el activo era un submenú, desactivar el estilo activo
            if self.active_button in [self.btn_sub_1, self.btn_sub_2, self.btn_sub_3]:
                self.active_button.setStyleSheet(SubMenuButton.SUB_BUTTON_BASE_STYLE)
                # Opcional: Volver a activar el botón padre como activo
                self.btn_home.setStyleSheet(MenuButton.NAV_BUTTON_ACTIVE_STYLE)
                self.btn_home.setText(self.HOME_TEXT_EXPANDED)  # Mantener flecha ▼ si queda activo
                self.active_button = self.btn_home

        else:
            # ABRIR
            start_height = self.height_collapsed
            end_height = required_height

            # 1. Desactivar el botón activo (si no es home)
            if self.active_button and self.active_button != self.btn_home:
                # Desactivar estilo del botón anterior
                if isinstance(self.active_button, MenuButton):
                    self.active_button.setStyleSheet(MenuButton.NAV_BUTTON_BASE_STYLE)
                elif isinstance(self.active_button, SubMenuButton):
                    self.active_button.setStyleSheet(SubMenuButton.SUB_BUTTON_BASE_STYLE)

            # 2. Establecer estilo y vista para 'Home'
            self.btn_home.setStyleSheet(MenuButton.NAV_BUTTON_ACTIVE_STYLE)
            self.btn_home.setText(self.HOME_TEXT_EXPANDED)  # Establecer flecha a expandido
            self.active_button = self.btn_home
            self.stacked_widget.setCurrentIndex(0)  # Siempre va a la vista de Inicio (Index 0)

        self.animation_submenu.setStartValue(start_height)
        self.animation_submenu.setEndValue(end_height)
        self.animation_submenu.start()

        self.is_expanded_sub = not self.is_expanded_sub

    def update_state_submenu(self):
        # Esta función solo se mantiene como callback de la animación (finished)
        pass

    def _change_view(self, button, index, parent_button=None):
        """
        Cambia la vista en el QStackedWidget y actualiza el estilo del botón activo.

        :param button: El botón que fue clickeado (el nuevo botón activo).
        :param index: El índice de la vista a mostrar.
        :param parent_button: Si es un submenú, el botón padre (ej: btn_home).
        """

        # No hacer nada si el botón ya está activo
        if self.active_button == button:
            return

        # 1. Desactivar el botón anterior
        if self.active_button:

            # Manejar el estilo del botón padre si el activo anterior era el padre
            if self.active_button == self.btn_home:
                # Si el submenú estaba abierto (is_expanded_sub), el estilo activo se mantendrá en el padre,
                # pero el texto debe indicar que el submenú está abierto, a menos que el nuevo botón no sea un hijo.

                # Desactivar el estilo activo del padre y cambiar el texto a base (sin flecha activa),
                # a menos que el submenú se quede abierto.
                if parent_button is None:  # Si el nuevo botón no es parte del submenú
                    self.active_button.setStyleSheet(MenuButton.NAV_BUTTON_BASE_STYLE)
                    self.active_button.setText(self.HOME_TEXT_BASE)

            elif isinstance(self.active_button, SubMenuButton):
                # Desactivar estilo del submenú anterior
                self.active_button.setStyleSheet(SubMenuButton.SUB_BUTTON_BASE_STYLE)

            elif isinstance(self.active_button, MenuButton):
                # Desactivar estilo del botón principal anterior (ej: btn_reports)
                self.active_button.setStyleSheet(MenuButton.NAV_BUTTON_BASE_STYLE)

            # Si el botón anterior no es el padre, pero el submenú está abierto, ciérralo forzadamente
            # Esto pasa si vienes de Reports y clicas Home, o viceversa. Pero esto ya lo maneja
            # toggle_submenu (al que se conecta btn_home). Solo hay que manejar el caso en que
            # clicas btn_reports mientras el submenú de btn_home está abierto.
            if parent_button is None and self.is_expanded_sub:
                self.toggle_submenu_collapse_only()

        # 2. Activar el nuevo botón
        if isinstance(button, MenuButton):
            # Es un botón de menú principal (ej: Reportes)
            button.setStyleSheet(MenuButton.NAV_BUTTON_ACTIVE_STYLE)

            # Si el botón principal no es HOME, asegúrate de que el texto de HOME sea solo base si no estaba expandido
            if button != self.btn_home:
                self.btn_home.setText(self.HOME_TEXT_BASE)

        elif isinstance(button, SubMenuButton):
            # Es un botón de submenú
            button.setStyleSheet(SubMenuButton.SUB_BUTTON_ACTIVE_STYLE)

            # Asegúrate de que el padre (btn_home) se mantenga en estilo activo y expandido si clicas un hijo
            if parent_button:
                parent_button.setStyleSheet(MenuButton.NAV_BUTTON_ACTIVE_STYLE)
                parent_button.setText(self.HOME_TEXT_EXPANDED)
                # Nota: No cambiamos self.active_button a parent_button, se queda como el hijo para saber cuál está seleccionado.

        self.active_button = button

        # 3. Cambiar la vista
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windos_dashboard = DashboardApp()
    windos_dashboard.show()
    sys.exit(app.exec())
