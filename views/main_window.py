import os
import sys
from views.utils_view.add_images import get_images_path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLabel, QFrame, QTableWidget, QTableWidgetItem, QHBoxLayout,
    QPushButton, QSizePolicy, QScrollArea
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
        sidebar.setMaximumHeight(60)

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

        # Content
        content = QFrame()
        content.setStyleSheet("background-color: transparent; border-top: 1px solid #b3b5b9;")
        layout_content = QHBoxLayout(content)
        layout_content.setContentsMargins(0,0,0,0)
        layout_content.setSpacing(0)

        content_nav = QFrame()
        content_nav.setStyleSheet("background-color: transparent; border-right: 1px solid #b3b5b9;")
        content_nav.setMinimumWidth(250)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("border: none;")

        # CONSTRUCCIÓN DE LA BARRA LATERAL (Conexión al change_view)
        # ------------------------------------------------------------------
        def _build_sidebar(self):
            """Construye la barra lateral completa con logo, usuario y menús."""
            self.sidebar = QFrame()
            self.sidebar.setMinimumWidth(self.expanded_width)
            self.sidebar.setMaximumWidth(self.expanded_width)
            self.sidebar.setStyleSheet("background-color: #2F3D55;")

            sidebar_main_layout = QVBoxLayout(self.sidebar)
            sidebar_main_layout.setContentsMargins(0, 0, 0, 0)
            sidebar_main_layout.setSpacing(0)

            # --- TOP HEADER (BOTÓN COLLAPSE) ---
            top_header = QFrame()
            top_header.setStyleSheet("background-color: #243147;")
            top_header_layout = QHBoxLayout(top_header)
            top_header_layout.setContentsMargins(5, 5, 5, 5)

            self.collapse_button = QPushButton()
            self.collapse_button.setIcon(QIcon("assets/icons/menu_toggle.png"))
            self.collapse_button.setIconSize(QSize(22, 22))
            self.collapse_button.setStyleSheet(
                "QPushButton {border: none; background-color: transparent;} QPushButton:hover {background-color: #3C4B64;}")
            self.collapse_button.clicked.connect(self.toggle_sidebar)

            top_header_layout.addWidget(self.collapse_button, alignment=Qt.AlignLeft)
            top_header_layout.addStretch(1)
            sidebar_main_layout.addWidget(top_header)

            # --- LOGO ---
            logo_frame = QFrame()
            logo_frame.setStyleSheet("background-color: #243147;")
            logo_layout = QVBoxLayout(logo_frame)
            logo_layout.setContentsMargins(15, 15, 15, 15)

            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "assets", "images", "apubyte.jpg")

            logo_pixmap = QPixmap(image_path)
            self.logo_label = QLabel()

            if not logo_pixmap.isNull():
                scaled_pixmap = logo_pixmap.scaled(
                    200, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.logo_label.setPixmap(scaled_pixmap)
                self.logo_label.setAlignment(Qt.AlignCenter)
                logo_layout.addWidget(self.logo_label)
            else:
                error_label = QLabel("Logo No Encontrado")
                error_label.setAlignment(Qt.AlignCenter)
                error_label.setStyleSheet("color: red; font-weight: bold;")
                logo_layout.addWidget(error_label)

            sidebar_main_layout.addWidget(logo_frame)

            # --- Cabecera de Usuario ---
            user_header = QWidget()
            user_header.setStyleSheet("background-color: #243147; padding: 10px; color: white;")
            user_layout = QVBoxLayout(user_header)

            self.user_label = QLabel("ADMIN")
            self.role_label = QLabel("EMPLEADO")

            user_layout.addWidget(self.user_label, alignment=Qt.AlignCenter)
            user_layout.addWidget(self.role_label, alignment=Qt.AlignCenter)
            sidebar_main_layout.addWidget(user_header)

            # --- Área de Desplazamiento para el Menú ---
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_area.setStyleSheet("border: none;")

            menu_container = QWidget()
            self.menu_scroll_layout = QVBoxLayout(menu_container)
            self.menu_scroll_layout.setAlignment(Qt.AlignTop)
            self.menu_scroll_layout.setContentsMargins(0, 0, 0, 0)
            self.menu_scroll_layout.setSpacing(0)
            scroll_area.setWidget(menu_container)

            # --- Menú Items CONECTADOS A change_view ---
            # NOTE: Pasamos self.change_view como click_handler a los botones simples
            item_inicio = create_simple_menu_item("Inicio", "assets/icons/home.png", is_selected=True,
                                                  click_handler=self.change_view)
            self.menu_scroll_layout.addWidget(item_inicio)

            # NOTE: La clase CollapseMenu ahora recibe 'parent' para acceder a change_view
            almacen_submenu = ["Categoría", "Presentacion", "Marca", "Producto", "Perecederos"]
            almacen_menu = CollapseMenu("Almacén", "assets/icons/almacen.png", almacen_submenu, parent=self)
            self.menu_scroll_layout.addWidget(almacen_menu)

            self.menu_scroll_layout.addWidget(
                create_simple_menu_item("Cotizaciones", "assets/icons/cotizaciones.png",
                                        click_handler=self.change_view))
            self.menu_scroll_layout.addWidget(
                create_simple_menu_item("Compras", "assets/icons/compras.png", click_handler=self.change_view))
            self.menu_scroll_layout.addWidget(
                create_simple_menu_item("Caja", "assets/icons/caja.png", click_handler=self.change_view))

            # BOTÓN DE VENTA CLAVE
            self.menu_scroll_layout.addWidget(
                create_simple_menu_item("Ventas", "assets/icons/ventas.png", click_handler=self.change_view))

            self.menu_scroll_layout.addWidget(
                create_simple_menu_item("Inventario", "assets/icons/inventario.png", click_handler=self.change_view))
            self.menu_scroll_layout.addWidget(
                create_simple_menu_item("Usuarios", "assets/icons/usuario.png", click_handler=self.change_view))
            self.menu_scroll_layout.addWidget(
                create_simple_menu_item("Parametros", "assets/icons/parametros.png", click_handler=self.change_view))

            sidebar_main_layout.addWidget(scroll_area)
            sidebar_main_layout.addStretch(1)









        content_view = QFrame()
        content_view.setStyleSheet("")

        layout_content.addWidget(content_nav, 1)
        layout_content.addWidget(content_view, 9)










        self.main_h_layout.addWidget(sidebar, 1)
        self.main_h_layout.addWidget(content, 9)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windos_dashboard = DashboardApp()
    windos_dashboard.show()
    sys.exit(app.exec())




