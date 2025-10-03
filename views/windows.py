import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QFrame, QHBoxLayout, QPushButton, QStackedWidget,
    QGridLayout, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox
)
from PySide6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QSize
)
from PySide6.QtGui import QFont, QColor


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


class SalesPage(QFrame):
    """Página de Punto de Venta (Index 4). Implementa la vista de 2 columnas solicitada."""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white; border-radius: 10px;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("PUNTO DE VENTA")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(title_label)

        # Contenedor Principal de 2 Columnas
        main_sales_container = QWidget()
        main_h_layout = QHBoxLayout(main_sales_container)
        main_h_layout.setSpacing(20)

        # ------------------- COLUMNA IZQUIERDA (PRODUCTOS Y DETALLE) -------------------
        left_column = QFrame()
        left_column_layout = QVBoxLayout(left_column)
        left_column_layout.setContentsMargins(0, 0, 0, 0)

        # 1. Buscador de Producto
        search_frame = QFrame()
        search_frame.setStyleSheet("background-color: #ECEFF1; border-radius: 8px; padding: 10px;")
        search_layout = QHBoxLayout(search_frame)

        search_label = QLabel("Buscar Producto:")
        search_input = QLineEdit()
        search_input.setPlaceholderText("Ingrese Código de Barras o Nombre...")
        search_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; background-color: white;")

        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        left_column_layout.addWidget(search_frame)

        # 2. Tabla de Detalles de Venta
        detail_table_title = QLabel("DETALLE DE VENTA")
        detail_table_title.setFont(QFont("Arial", 12, QFont.Bold))
        detail_table_title.setStyleSheet("margin-top: 15px; margin-bottom: 5px;")
        left_column_layout.addWidget(detail_table_title)

        self.sales_detail_table = QTableWidget()
        self._setup_sales_detail_table(self.sales_detail_table)
        left_column_layout.addWidget(self.sales_detail_table)

        main_h_layout.addWidget(left_column, 2)  # 2/3 del ancho

        # ------------------- COLUMNA DERECHA (CLIENTE Y TOTALES) -------------------
        right_column = QFrame()
        right_column.setFixedWidth(350)
        right_column_layout = QVBoxLayout(right_column)
        right_column_layout.setContentsMargins(0, 0, 0, 0)
        right_column_layout.setSpacing(15)

        # Función auxiliar para crear cajas de métricas (simplificado para esta clase)
        def create_sales_metric_box(title, value, color_hex, font_size=16):
            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{ 
                    background-color: {color_hex}; 
                    border-radius: 8px; 
                    color: white;
                    padding: 15px;
                }}
            """)
            layout = QVBoxLayout(frame)
            value_label = QLabel(value)
            value_label.setFont(QFont("Arial", font_size, QFont.Bold))
            title_label = QLabel(title)
            title_label.setFont(QFont("Arial", 9))
            layout.addWidget(value_label)
            layout.addWidget(title_label)
            return frame

        # 1. Selector de Cliente
        client_frame = QFrame()
        client_frame.setStyleSheet("background-color: #E6EAF0; border-radius: 8px; padding: 15px;")
        client_layout = QVBoxLayout(client_frame)
        client_layout.addWidget(QLabel("Cliente Seleccionado:", styleSheet="font-weight: bold;"))

        client_combo = QComboBox()
        client_combo.addItems(["Público General", "Cliente Frecuente A", "Cliente Nuevo B"])
        client_combo.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px; background-color: white;")
        client_layout.addWidget(client_combo)

        right_column_layout.addWidget(client_frame)

        # 2. Resumen de Totales
        right_column_layout.addWidget(create_sales_metric_box("SUBTOTAL", "$ 4,000.00", "#5BC0DE"))
        right_column_layout.addWidget(create_sales_metric_box("DESCUENTO", "$ 0.00", "#F0AD4E"))

        # Total Grande
        total_box = create_sales_metric_box("TOTAL A PAGAR", "$ 4,000.00", "#2ECC71", 24)
        total_box.setFixedHeight(120)
        right_column_layout.addWidget(total_box)

        # 3. Botones de Acción
        action_button_style = "QPushButton { padding: 15px; border-radius: 8px; font-weight: bold; font-size: 11pt; color: white; }"

        btn_pay = QPushButton("PAGAR VENTA (F1)")
        btn_pay.setStyleSheet(
            action_button_style + "background-color: #007BFF; QPushButton:hover { background-color: #0056b3; }")

        btn_cancel = QPushButton("CANCELAR VENTA (Esc)")
        btn_cancel.setStyleSheet(
            action_button_style + "background-color: #E74C3C; QPushButton:hover { background-color: #c0392b; }")

        right_column_layout.addWidget(btn_pay)
        right_column_layout.addWidget(btn_cancel)
        right_column_layout.addStretch(1)

        main_h_layout.addWidget(right_column, 1)

        main_layout.addWidget(main_sales_container)
        main_layout.addStretch(1)

    def _setup_sales_detail_table(self, table_widget):
        """Configura la tabla de detalles de venta con datos de ejemplo."""
        headers = ["Código", "Producto", "Cantidad", "Precio Unitario", "Subtotal"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)

        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        table_widget.setStyleSheet("QTableWidget { background-color: #FAFAFA; border: 1px solid #DDD; }")

        table_data = [
            ["04022343", "GALLETA OREO", "2", "1.50", "3.00"],
            ["99000000", "PARACETAMOL 500mg", "10", "4.00", "40.00"],
            ["123456789", "COCA COLA 2L", "1", "26.00", "26.00"],
        ]

        table_widget.setRowCount(len(table_data))
        for i, row in enumerate(table_data):
            for j, item in enumerate(row):
                table_item = QTableWidgetItem(item)
                table_item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(i, j, table_item)

        table_widget.resizeColumnsToContents()
        table_widget.horizontalHeader().setStretchLastSection(True)


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
        self.is_expanded = False
        self.is_submenu_expanded = False
        self.width_collapsed = 50
        self.width_expanded = 250
        self.current_page = 0

        # Layout Principal: Vertical (Header, Content)
        self.main_v_layout = QVBoxLayout(main_widget)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.main_v_layout.setSpacing(0)

        # --- HEADER (Barra Superior) ---
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: transparent;")
        layout_sidebar = QHBoxLayout(sidebar)

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
        header_layout.addWidget(QLabel("Admin: Rodrigo .F", styleSheet="color: white;"),
                                alignment=Qt.AlignmentFlag.AlignRight)

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
        self.nav_layout = QVBoxLayout(self.content_nav)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(5)

        # Área de Contenido Principal (Stacked Widget)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(DashboardPage())  # Índice 0: Inicio
        self.stacked_widget.addWidget(CategoryPage())  # Índice 1: Categoría
        self.stacked_widget.addWidget(ProductPage())  # Índice 2: Producto
        self.stacked_widget.addWidget(UsersPage())  # Índice 3: Usuarios
        self.stacked_widget.addWidget(SalesPage())  # <-- Índice 4: Ventas (NUEVO)

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

        # --- Contenedor de Submenús ---
        self.almacen_submenu_container = QFrame()
        self.almacen_submenu_container.setMaximumHeight(0)
        self.almacen_submenu_container.setStyleSheet("background-color: #3e5a75; border-left: 5px solid #1abc9c;")
        submenu_layout = QVBoxLayout(self.almacen_submenu_container)
        submenu_layout.setContentsMargins(0, 0, 0, 0)
        submenu_layout.setSpacing(0)

        # Submenús de Almacen (Índices 1 y 2)
        self.sub_btn_category = self.create_nav_button("  ", "Categoría", 1, is_child=True)
        self.sub_btn_product = self.create_nav_button("  ", "Productos", 2, is_child=True)

        # 3. Botón Usuarios (Simple Page Button)
        self.btn_users = self.create_nav_button("👥", "Usuarios", 3)

        # 4. Botón Ventas (NUEVO - Índice 4)
        self.btn_sales = self.create_nav_button("🛒", "Ventas", 4)  # <-- NUEVO BOTÓN

        # --- Conexiones de Navegación ---
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        self.sub_btn_category.clicked.connect(lambda: self.switch_page(1))
        self.sub_btn_product.clicked.connect(lambda: self.switch_page(2))
        self.btn_users.clicked.connect(lambda: self.switch_page(3))
        self.btn_sales.clicked.connect(lambda: self.switch_page(4))  # <-- CONEXIÓN NUEVA

        # --- Ensamblaje del Layout ---
        btn_layout.addWidget(self.btn_dashboard)
        btn_layout.addWidget(self.btn_almacen)
        btn_layout.addWidget(self.almacen_submenu_container)

        # Insertar los nuevos botones en el layout principal
        btn_layout.addWidget(self.btn_sales)  # <-- NUEVA POSICIÓN
        btn_layout.addWidget(self.btn_users)

        btn_layout.addStretch(1)

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
        full_text = f"{icon} {text}"
        if is_parent:
            # Añade el ícono de colapso al texto completo (inicialmente cerrado)
            full_text += "  ►"

        btn = QPushButton(full_text)
        btn.setObjectName(f"nav_btn_{index}")
        btn.setProperty("full_text", full_text)
        btn.setProperty("nav_index", index)
        btn.setProperty("is_parent", is_parent)

        btn.setFixedHeight(45)
        btn.setFont(QFont("Roboto", 12))

        style = f"""
            QPushButton#nav_btn_{index} {{
                color: white; 
                background-color: transparent;
                border: none;
                text-align: left;
                padding-left: 10px;
        """
        if is_child:
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

        buttons = [self.btn_dashboard, self.btn_almacen, self.btn_users, self.btn_sales,
                   self.sub_btn_category, self.sub_btn_product]

        for btn in buttons:
            full_text = btn.property("full_text")
            is_parent = btn.property("is_parent")

            # --- Lógica de Colapso HORIZONTAL ---
            if self.is_expanded:
                btn.setText(full_text)
                btn.setFixedWidth(self.width_expanded)
            else:
                icon = full_text.split()[0]
                if is_parent:
                    # Si es padre colapsado, muestra solo la caja ("📦")
                    icon = icon[:-2]

                btn.setText(icon)
                btn.setFixedWidth(self.width_collapsed)

            # --- Lógica de Estilo Activo ---
            is_active_page = self.stacked_widget.currentIndex() == btn.property("nav_index")
            # El padre es activo si su submenú está visible
            is_parent_active = is_parent and self.is_submenu_expanded

            current_style = btn.styleSheet().split("}")[0]

            if is_active_page or is_parent_active:
                btn.setStyleSheet(current_style + "background-color: #1abc9c; }")
            else:
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

        self.animation.setStartValue(start_width)
        self.animation.setEndValue(end_width)
        self.animation.start()

        self.is_expanded = not self.is_expanded
        self.update_nav_styles()
        self.is_expanded = not self.is_expanded

    def update_state(self):
        """Invierte el estado HORIZONTAL cuando la animación finaliza."""
        self.is_expanded = not self.is_expanded
        self.update_nav_styles()

    def toggle_submenu(self):
        """Lógica de alternancia (toggle) para el submenú de Almacen (Vertical)."""

        # Calcular la altura de los submenús (2 hijos * 45px de altura)
        required_height = self.sub_btn_category.height() * 2

        if self.is_submenu_expanded:
            start_height = required_height
            end_height = 0
            # Cambia de ▼ a ► (Flecha de cerrado)
            self.btn_almacen.setText(self.btn_almacen.property("full_text").replace("▼", "►"))
            self.btn_almacen.setProperty("full_text", self.btn_almacen.property("full_text").replace("▼", "►"))
        else:
            start_height = 0
            end_height = required_height
            # Cambia de ► a ▼ (Flecha de abierto)
            self.btn_almacen.setText(self.btn_almacen.property("full_text").replace("►", "▼"))
            self.btn_almacen.setProperty("full_text", self.btn_almacen.property("full_text").replace("►", "▼"))

        self.submenu_animation.setStartValue(start_height)
        self.submenu_animation.setEndValue(end_height)
        self.submenu_animation.start()

        self.is_submenu_expanded = not self.is_submenu_expanded
        self.update_nav_styles()

    def switch_page(self, index):
        """Cambia el widget visible en el StackedWidget."""
        self.stacked_widget.setCurrentIndex(index)
        self.current_page = index
        self.update_nav_styles()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_dashboard = DashboardApp()
    window_dashboard.show()
    sys.exit(app.exec())
