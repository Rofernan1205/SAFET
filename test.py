import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QFrame, QHBoxLayout, QPushButton, QStackedWidget
)
from PySide6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QSize
)
from PySide6.QtGui import QFont


# --- CLASES DE PÁGINAS DE CONTENIDO (SIMULACIÓN) ---

class DashboardPage(QFrame):
    """Página de ejemplo para el Dashboard (Index 0)."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f0f4f7;")
        layout = QVBoxLayout(self)
        label = QLabel("PANEL PRINCIPAL (DASHBOARD)")
        label.setStyleSheet("font-size: 24px; color: #2c3e50;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


class CategoryPage(QFrame):
    """Página de ejemplo para Categorías (Index 1)."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fce4ec;")
        layout = QVBoxLayout(self)
        label = QLabel("GESTIÓN DE CATEGORÍAS")
        label.setStyleSheet("font-size: 24px; color: #9c27b0;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


class ProductPage(QFrame):
    """Página de ejemplo para Productos (Index 2)."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #e8f5e9;")
        layout = QVBoxLayout(self)
        label = QLabel("GESTIÓN DE PRODUCTOS")
        label.setStyleSheet("font-size: 24px; color: #4caf50;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


class UsersPage(QFrame):
    """Página de ejemplo para Gestión de Usuarios (Index 3)."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #e6f0ff;")
        layout = QVBoxLayout(self)
        label = QLabel("GESTIÓN DE USUARIOS")
        label.setStyleSheet("font-size: 24px; color: #2c3e50;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)


# --- CLASE PRINCIPAL ---

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAFET - DashBoard")
        self.resize(1000, 700)

        self.setStyleSheet("background-color: #34495e;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 1. Variables de Estado
        self.is_expanded = False  # Estado del colapso HORIZONTAL (Sidebar)
        self.is_submenu_expanded = False  # Estado del colapso VERTICAL (Almacen)
        self.width_collapsed = 50
        self.width_expanded = 250
        self.current_page = 0

        # Layout Principal: Vertical (Header, Content)
        self.main_v_layout = QVBoxLayout(main_widget)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.main_v_layout.setSpacing(0)

        # --- HEADER (Barra Superior - Configuración Simplificada) ---
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: transparent;")
        layout_sidebar = QHBoxLayout(sidebar)
        # ... (Configuración de Header simplificada) ...

        box_logo = QFrame()
        layout_logo = QHBoxLayout(box_logo)
        word_logo = QLabel("SATEF")
        word_logo.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        layout_logo.addWidget(word_logo)

        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.clicked.connect(self.toggle_panel)
        self.toggle_btn.setFixedSize(30, 30)
        self.toggle_btn.setStyleSheet("""
        QPushButton { color: white; border: 1px solid white; border-radius: 5px; background-color: transparent;}
        QPushButton:hover { background-color: #9198a1;}
        """)

        header_controls = QFrame()
        header_layout = QHBoxLayout(header_controls)
        header_layout.addWidget(box_logo)
        header_layout.addWidget(self.toggle_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        header_layout.addStretch(1)
        header_layout.addWidget(QLabel("Admin: Rodrigo .F"), alignment=Qt.AlignmentFlag.AlignRight)

        layout_sidebar.addWidget(header_controls)

        # --- CONTENT (Barra de Navegación + Vista Principal) ---
        content = QFrame()
        content.setStyleSheet("background-color: transparent; border-top: 1px solid #b3b5b9;")
        self.layout_content = QHBoxLayout(content)
        self.layout_content.setContentsMargins(0, 0, 0, 0)
        self.layout_content.setSpacing(0)

        # Widget de Navegación (EL QUE ANIMAREMOS HORIZONTALMENTE)
        self.content_nav = QFrame()
        self.content_nav.setStyleSheet("background-color: #2c3e50; border-right: 1px solid #b3b5b9;")
        self.content_nav.setMinimumWidth(self.width_collapsed)
        self.nav_layout = QVBoxLayout(self.content_nav)  # Layout interno para botones
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(5)  # Añadir espaciado entre botones

        # Área de Contenido Principal (Stacked Widget)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(DashboardPage())  # Índice 0: Inicio
        self.stacked_widget.addWidget(CategoryPage())  # Índice 1: Categoría
        self.stacked_widget.addWidget(ProductPage())  # Índice 2: Producto
        self.stacked_widget.addWidget(UsersPage())  # Índice 3: Usuarios

        # Ensamblar Content
        self.layout_content.addWidget(self.content_nav, 0)
        self.layout_content.addWidget(self.stacked_widget, 1)

        self.main_v_layout.addWidget(sidebar, 1)
        self.main_v_layout.addWidget(content, 9)

        # --- 2. CONFIGURACIÓN DE LOS BOTONES DE MENÚ ---
        self.setup_nav_buttons()

        # --- 3. CONFIGURACIÓN DEL ANIMADOR HORIZONTAL (Sidebar) ---
        self.animation = QPropertyAnimation(self.content_nav, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.finished.connect(self.update_state)

        # --- 4. CONFIGURACIÓN DEL ANIMADOR VERTICAL (Submenú) ---
        # Este se configura después de crear el contenedor del submenú en setup_nav_buttons

    def setup_nav_buttons(self):
        """Crea la estructura del menú, incluyendo el submenú de Almacen."""
        btn_container = QFrame()
        btn_layout = QVBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(5)

        # 1. Botón Inicio (Simple Page Button)
        self.btn_dashboard = self.create_nav_button("🏠", "Inicio", 0)

        # 2. Almacen (Parent Toggle Button)
        self.btn_almacen = self.create_nav_button("📦", "Almacen", -1, is_parent=True)
        self.btn_almacen.clicked.connect(self.toggle_submenu)

        # --- Contenedor de Submenús (Verticalmente Colapsable) ---
        self.almacen_submenu_container = QFrame()
        # Inicialmente cerrado
        self.almacen_submenu_container.setMaximumHeight(0)
        self.almacen_submenu_container.setStyleSheet("background-color: #3e5a75; border-left: 5px solid red;")
        submenu_layout = QVBoxLayout(self.almacen_submenu_container)
        submenu_layout.setContentsMargins(0, 0, 0, 0)
        submenu_layout.setSpacing(0)

        # Submenús de Almacen (Índices 1 y 2)
        self.sub_btn_category = self.create_nav_button("  ", "Categoría", 1, is_child=True)
        self.sub_btn_product = self.create_nav_button("  ", "Productos", 2, is_child=True)

        # 3. Botón Usuarios (Simple Page Button)
        self.btn_users = self.create_nav_button("👥", "Usuarios", 3)

        # --- Conexiones de Navegación ---
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        self.sub_btn_category.clicked.connect(lambda: self.switch_page(1))
        self.sub_btn_product.clicked.connect(lambda: self.switch_page(2))
        self.btn_users.clicked.connect(lambda: self.switch_page(3))

        # --- Ensamblaje del Layout ---
        btn_layout.addWidget(self.btn_dashboard)
        btn_layout.addWidget(self.btn_almacen)
        btn_layout.addWidget(self.almacen_submenu_container)  # Contenedor vertical
        btn_layout.addWidget(self.btn_users)
        btn_layout.addStretch(1)  # Empuja los botones hacia arriba

        # Ensamblaje de los Submenús
        submenu_layout.addWidget(self.sub_btn_category)
        submenu_layout.addWidget(self.sub_btn_product)

        self.nav_layout.addWidget(btn_container)

        # --- 4. Inicialización del Animador VERTICAL ---
        self.submenu_animation = QPropertyAnimation(self.almacen_submenu_container, b"maximumHeight")
        self.submenu_animation.setDuration(200)
        self.submenu_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Llamar para establecer el estilo inicial correcto de los botones
        self.update_nav_styles()

    def create_nav_button(self, icon, text, index, is_parent=False, is_child=False):
        """Crea un botón de navegación, ajustando el estilo según si es padre o hijo."""

        # El texto completo se almacena como propiedad para la expansión horizontal
        full_text = f"{icon} {text}"
        if is_parent:
            full_text += "  ▼"  # Añade el ícono de colapso al texto completo

        btn = QPushButton(full_text)
        btn.setObjectName(f"nav_btn_{index}")
        btn.setProperty("full_text", full_text)  # Guarda el texto completo para referencia
        btn.setProperty("nav_index", index)  # Guarda el índice de la página
        btn.setProperty("is_parent", is_parent)

        btn.setFixedHeight(45)
        btn.setFont(QFont("Roboto", 12))

        # Estilo CSS base
        style = f"""
            QPushButton#nav_btn_{index} {{
                color: white; 
                background-color: transparent;
                border: none;
                text-align: left;
                padding-left: 10px;
        """
        if is_child:
            # Los hijos tienen más margen para simular anidamiento
            style += "padding-left: 30px; "

        style += f"""
            }}
            QPushButton#nav_btn_{index}:hover {{
                background-color: #34495e; 
            }}
        """
        btn.setStyleSheet(style)

        return btn

    def update_nav_styles(self):
        """Actualiza el texto, el ancho y el estilo activo de todos los botones."""

        # 1. Ajustar los botones para la expansión/colapso HORIZONTAL
        buttons = [self.btn_dashboard, self.btn_almacen, self.btn_users,
                   self.sub_btn_category, self.sub_btn_product]

        for btn in buttons:
            full_text = btn.property("full_text")
            is_parent = btn.property("is_parent")

            # --- Lógica de Colapso HORIZONTAL ---
            if self.is_expanded:
                # Mostrar texto y forzar ancho expandido
                btn.setText(full_text)
                btn.setFixedWidth(self.width_expanded)
            else:
                # Ocultar texto (mostrar solo el primer carácter: el icono)
                icon = full_text.split()[0]
                # Si es padre, ajustamos el ícono de colapso vertical si está en el texto
                if is_parent:
                    icon = icon[:-2]  # Quita '  ▼' para dejar solo el icono principal

                btn.setText(icon)
                btn.setFixedWidth(self.width_collapsed)

            # --- Lógica de Estilo Activo ---
            is_active_page = self.stacked_widget.currentIndex() == btn.property("nav_index")
            is_parent_active = is_parent and self.is_submenu_expanded

            current_style = btn.styleSheet().split("}")[0]  # Tomar solo el estilo base

            if is_active_page or is_parent_active:
                # Si la página está activa o es el padre activo (Almacen)
                btn.setStyleSheet(current_style + "background-color: #1abc9c; }")
            else:
                # Estilo normal (hover)
                btn.setStyleSheet(current_style + "background-color: transparent; }")

    # --- MÉTODOS DE ANIMACIÓN Y NAVEGACIÓN ---

    def toggle_panel(self):
        """Lógica de alternancia (toggle) para la barra lateral (Horizontal)."""
        if self.is_expanded:
            start_width = self.width_expanded
            end_width = self.width_collapsed
            self.toggle_btn.setText("☰")
        else:
            start_width = self.width_collapsed
            end_width = self.width_expanded
            self.toggle_btn.setText("←")

        # Configurar y ejecutar animación horizontal
        self.animation.setStartValue(start_width)
        self.animation.setEndValue(end_width)
        self.animation.start()

        # Anticipamos el cambio de estado para que update_nav_styles sepa la próxima acción
        self.is_expanded = not self.is_expanded
        self.update_nav_styles()
        self.is_expanded = not self.is_expanded  # Revertimos temporalmente

    def update_state(self):
        """Invierte el estado HORIZONTAL cuando la animación finaliza."""
        self.is_expanded = not self.is_expanded
        self.update_nav_styles()

    def toggle_submenu(self):
        """Lógica de alternancia (toggle) para el submenú de Almacen (Vertical)."""

        if self.is_submenu_expanded:
            # Colapsar: Animar a altura 0
            start_height = self.almacen_submenu_container.height()
            end_height = 0
            # Actualizar flecha de Almacen
            self.btn_almacen.setText(self.btn_almacen.property("full_text").replace("▼", "►"))
        else:
            # Expandir: Calcular altura requerida para mostrar todos los submenús
            # Sumar la altura de cada botón + el espaciado
            # (Aquí asumimos que los botones tienen 45px de altura)
            required_height = self.sub_btn_category.height() * 2

            start_height = 0
            end_height = required_height
            # Actualizar flecha de Almacen
            self.btn_almacen.setText(self.btn_almacen.property("full_text").replace("►", "▼"))

        self.submenu_animation.setStartValue(start_height)
        self.submenu_animation.setEndValue(end_height)
        self.submenu_animation.start()

        # Invertir el estado vertical
        self.is_submenu_expanded = not self.is_submenu_expanded
        self.update_nav_styles()  # Actualizar estilos de los hijos

    def switch_page(self, index):
        """Cambia el widget visible en el StackedWidget."""
        self.stacked_widget.setCurrentIndex(index)
        self.current_page = index
        self.update_nav_styles()  # Refresca los estilos para marcar el botón activo


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_dashboard = DashboardApp()
    window_dashboard.show()
    sys.exit(app.exec())
