import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLabel, QFrame, QTableWidget, QTableWidgetItem, QHBoxLayout,
    QPushButton, QSizePolicy, QSlider, QScrollArea, QLineEdit, QComboBox
)
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor, QScreen
from PySide6.QtCore import Qt, QSize, QRect, QPropertyAnimation, QEasingCurve, QLocale


# ========================================================
# 1. SIMULACIÓN DE LA CAPA DE DATOS (SQLAlchemy ORM)
# ========================================================
def obtener_datos_dashboard_simulados():
    """Función simulada que obtendría datos reales de la base de datos."""
    return {
        "caja_actual": "$ 84.00",
        "proveedores": "6.00",
        "articulos_agotados": "64.00",
        "compras_mes": "$ 1,494.21",
        "marcas": "19.00",
        "vencen_30_dias": "0.00",
        "ventas_dia": "$ 4.00",
        "promociones": "12.00",
        "clientes": "41.00",
        "stock_invertido": "$ 24,999,221",
        "productos_reg": "92.00",
        "creditos_pagares": "20.00",
    }


# ========================================================
# 2. WIDGETS REUTILIZABLES DE LA INTERFAZ (UI)
# ========================================================
def create_metric_box(title, value, color_hex):
    """Crea el recuadro de métrica con colores y formato."""
    frame = QFrame()
    frame.setStyleSheet(f"""
        QFrame {{ 
            background-color: {color_hex}; 
            border-radius: 8px; 
            color: white;
            padding: 15px;
        }}
    """)
    frame.setFixedSize(220, 100)

    layout = QVBoxLayout(frame)
    layout.setSpacing(5)

    locale = QLocale(QLocale.Spanish)
    try:
        # Intenta formatear el valor como moneda si contiene '$' o parece numérico
        if value.replace('$', '').replace('.', '').replace(',', '').strip().isdigit():
            clean_value = value.replace('$', '').replace(',', '')
            formatted_value = locale.toString(float(clean_value), 'f', 2)
            if '$' in value:
                value_display = f"$ {formatted_value}"
            else:
                value_display = formatted_value
        else:
            value_display = value
    except:
        value_display = value

    value_label = QLabel(value_display)
    value_label.setFont(QFont("Arial", 16, QFont.Bold))

    title_label = QLabel(title)
    title_label.setFont(QFont("Arial", 9))

    layout.addWidget(value_label)
    layout.addWidget(title_label)

    return frame


class CollapseMenu(QWidget):
    """Widget que maneja la lógica de un menú desplegable (Acordeón)."""

    def __init__(self, title, icon_path, submenu_items, parent=None):
        super().__init__(parent)
        self.is_collapsed = True
        self.item_text = title  # Almacenamos el texto completo para el toggle

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.header_button = self._create_header_button(title, icon_path)
        self.header_button.clicked.connect(self.toggle_collapse)
        self.main_layout.addWidget(self.header_button)

        self.submenu_container = QWidget()
        self.submenu_layout = QVBoxLayout(self.submenu_container)
        self.submenu_layout.setContentsMargins(15, 0, 0, 0)
        self.submenu_layout.setSpacing(0)

        for item_text in submenu_items:
            # Los submenús también deben tener una conexión para cambiar de vista
            sub_button = self._create_submenu_button(item_text, parent.change_view)
            self.submenu_layout.addWidget(sub_button)

        self.submenu_container.hide()
        self.main_layout.addWidget(self.submenu_container)

    def _create_header_button(self, text, icon_path):
        """Crea el botón principal con estilo para el menú lateral."""
        btn = QPushButton(text)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(22, 22))

        # Necesitamos almacenar el texto aquí también para que el toggle funcione en el submenú
        btn.item_text = text

        btn.setStyleSheet("""
            QPushButton { 
                text-align: left; 
                padding: 10px 10px 10px 5px; 
                background-color: #2F3D55; 
                border: none;
                color: #ccc; 
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #007BFF; 
                color: white;
            }
        """)
        return btn

    def _create_submenu_button(self, text, change_view_callback):
        """Crea un botón simple para el submenú y lo conecta."""
        btn = QPushButton(text)
        btn.item_text = text  # Guardamos el texto
        btn.clicked.connect(lambda: change_view_callback(text))
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 5px 10px;
                background-color: #3C4B64;
                border: none;
                color: #ccc;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #4C5D76;
                color: white;
            }
        """)
        return btn

    def toggle_collapse(self):
        """Alterna la visibilidad del submenú al hacer clic."""
        if self.is_collapsed:
            self.submenu_container.show()
            self.is_collapsed = False
        else:
            self.submenu_container.hide()
            self.is_collapsed = True


def create_simple_menu_item(text, icon_path, is_selected=False, click_handler=None):
    """Crea un ítem de menú simple que no se colapsa."""
    btn = QPushButton(text)
    btn.setIcon(QIcon(icon_path))
    btn.setIconSize(QSize(22, 22))

    btn.item_text = text  # <-- CLAVE: Guardamos el texto completo para el toggle
    if click_handler:
        # Conecta el botón a la función de cambio de vista, pasándole el texto del botón
        btn.clicked.connect(lambda: click_handler(text))

    style = """
        QPushButton { 
            text-align: left; 
            padding: 10px 10px 10px 5px; 
            border: none;
            font-size: 11pt;
        }
    """
    if is_selected:
        btn.setObjectName("active_menu")
        style += "QPushButton#active_menu { background-color: #007BFF; color: white; }"
    else:
        btn.setObjectName("")
        style += "QPushButton { background-color: #2F3D55; color: #ccc; }"
        style += "QPushButton:hover { background-color: #3C4B64; color: white; }"

    btn.setStyleSheet(style)
    return btn


# ========================================================
# 3. VENTANA PRINCIPAL DE LA APLICACIÓN
# ========================================================

class DashboardApp(QMainWindow):
    # ------------------------------------------------------------------
    # PASO 1: Inicialización y Variables de Colapso
    # ------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAFET - Sistema de Ventas e Inventario")

        # --- Variables de Estado para el Colapso ---
        self.is_sidebar_expanded = True
        self.expanded_width = 230
        self.collapsed_width = 60
        self.current_active_button = None  # Referencia al botón activo

        # 1. Establecer el tamaño y centrar la ventana
        self.setGeometry(100, 100, 1300, 900)
        self.center_window()

        # --- Configuración de Layouts ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout Principal: Horizontal (Sidebar | Contenido)
        self.main_h_layout = QHBoxLayout(main_widget)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_h_layout.setSpacing(0)

        self._build_sidebar()

        self.content_area = QWidget()
        self.content_area_layout = QVBoxLayout(self.content_area)
        self.content_area_layout.setContentsMargins(15, 15, 15, 15)

        # Iniciar en la vista de Dashboard
        self.change_view("Inicio")

        # Añadir al Layout Maestro
        self.main_h_layout.addWidget(self.sidebar)
        self.main_h_layout.addWidget(self.content_area, 1)

    # ------------------------------------------------------------------
    # NAVEGACIÓN Y VISTAS
    # ------------------------------------------------------------------
    def change_view(self, view_name):
        """Cambia la vista principal según el botón del menú presionado."""

        # 1. Limpiar la vista anterior
        while self.content_area_layout.count():
            item = self.content_area_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 2. Resaltar el botón activo
        self._set_active_button(view_name)

        # 3. Construir la nueva vista
        if view_name == "Inicio":
            self._build_dashboard()
        elif view_name == "Ventas":
            self._build_sales_view()
        # Puedes añadir más vistas aquí (ej: elif view_name == "Inventario": ...)
        else:
            # Vista por defecto/genérica para otros botones
            self._build_generic_view(view_name)

    def _set_active_button(self, view_name):
        """Busca el botón en el menú y aplica el estilo activo."""

        # Desactivar el botón anterior
        if self.current_active_button:
            self.current_active_button.setObjectName("")
            self.current_active_button.setStyleSheet(
                self.current_active_button.styleSheet().replace("background-color: #007BFF; color: white;",
                                                                "background-color: #2F3D55; color: #ccc;"))

        # Buscar y activar el nuevo botón
        for i in range(self.menu_scroll_layout.count()):
            widget = self.menu_scroll_layout.itemAt(i).widget()

            # Chequea ítems simples
            if isinstance(widget, QPushButton) and widget.item_text == view_name:
                self.current_active_button = widget
                break

            # Chequea ítems en CollapseMenu
            elif isinstance(widget, CollapseMenu):
                # Chequea el header del collapse
                if widget.header_button.item_text == view_name:
                    self.current_active_button = widget.header_button
                    break
                # Chequea los sub-ítems
                for j in range(widget.submenu_layout.count()):
                    sub_btn = widget.submenu_layout.itemAt(j).widget()
                    if isinstance(sub_btn, QPushButton) and sub_btn.item_text == view_name:
                        self.current_active_button = sub_btn
                        break
                if self.current_active_button and self.current_active_button != widget.header_button:
                    break

        # Aplicar estilo activo si se encontró un botón
        if self.current_active_button:
            self.current_active_button.setObjectName("active_menu")
            self.current_active_button.setStyleSheet(
                self.current_active_button.styleSheet().replace("background-color: #2F3D55; color: #ccc;",
                                                                "background-color: #007BFF; color: white;"))

            # Asegura que los botones de submenú que no son el header usen su propio color de fondo
            if self.current_active_button.parent() and self.current_active_button.parent().parent() and self.current_active_button.parent().parent().isHidden():
                self.current_active_button.parent().parent().show()  # Despliega el menú si estaba colapsado

    # ------------------------------------------------------------------
    # FUNCIÓN DE CENTRADO DE VENTANA
    # ------------------------------------------------------------------
    def center_window(self):
        """Calcula y aplica la posición para centrar la ventana en la pantalla."""
        window_rect = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        window_rect.moveCenter(center_point)
        self.move(window_rect.topLeft())

    # ------------------------------------------------------------------
    # LÓGICA DE COLAPSO (toggle_sidebar) - Sin cambios
    # ------------------------------------------------------------------
    def toggle_sidebar(self):
        """Alterna entre el estado expandido y colapsado de la barra lateral."""
        target_width = self.collapsed_width if self.is_sidebar_expanded else self.expanded_width
        self.animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.sidebar.width())
        self.animation.setEndValue(target_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(self._update_menu_text_visibility)
        self.animation.start()
        self.is_sidebar_expanded = not self.is_sidebar_expanded

    # ------------------------------------------------------------------
    # LÓGICA DE VISIBILIDAD DE TEXTO (_update_menu_text_visibility) - Sin cambios
    # ------------------------------------------------------------------
    def _update_menu_text_visibility(self):
        """Muestra u oculta el texto de todos los botones y el logo."""
        for i in range(self.menu_scroll_layout.count()):
            item_widget = self.menu_scroll_layout.itemAt(i).widget()

            if item_widget and isinstance(item_widget, (QPushButton, CollapseMenu)):
                btn = item_widget
                if isinstance(item_widget, CollapseMenu):
                    btn = item_widget.header_button

                if self.is_sidebar_expanded:
                    btn.setText(btn.item_text)
                    btn.setToolTip("")
                    btn.setStyleSheet(btn.styleSheet().replace("text-align: center", "text-align: left"))
                else:
                    btn.setText("")
                    btn.setToolTip(btn.item_text)
                    btn.setStyleSheet(btn.styleSheet().replace("text-align: left", "text-align: center"))

        self.user_label.setVisible(self.is_sidebar_expanded)
        self.role_label.setVisible(self.is_sidebar_expanded)
        self.logo_label.setVisible(self.is_sidebar_expanded)

    # ------------------------------------------------------------------
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
            create_simple_menu_item("Cotizaciones", "assets/icons/cotizaciones.png", click_handler=self.change_view))
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

    # ------------------------------------------------------------------
    # FUNCIÓN DE VISTA DE VENTAS (NUEVO)
    # ------------------------------------------------------------------
    def _build_sales_view(self):
        """Construye la vista de Ventas con el formato solicitado (2 Columnas)."""

        title_label = QLabel("PUNTO DE VENTA")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.content_area_layout.addWidget(title_label)

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
        search_frame.setStyleSheet("background-color: #E6EAF0; border-radius: 8px; padding: 10px;")
        search_layout = QHBoxLayout(search_frame)

        search_label = QLabel("Buscar Producto:")
        search_input = QLineEdit()
        search_input.setPlaceholderText("Ingrese Código de Barras o Nombre...")
        search_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

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
        right_column.setFixedWidth(400)  # Ancho fijo para la columna de totales
        right_column_layout = QVBoxLayout(right_column)
        right_column_layout.setContentsMargins(0, 0, 0, 0)
        right_column_layout.setSpacing(10)

        # 1. Selector de Cliente
        client_frame = QFrame()
        client_frame.setStyleSheet("background-color: #E6EAF0; border-radius: 8px; padding: 15px;")
        client_layout = QVBoxLayout(client_frame)
        client_layout.addWidget(QLabel("Cliente Seleccionado:"))

        client_combo = QComboBox()
        client_combo.addItems(["Público General", "Cliente Frecuente A", "Cliente Nuevo B"])
        client_combo.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")
        client_layout.addWidget(client_combo)

        right_column_layout.addWidget(client_frame)

        # 2. Resumen de Totales (Métricas)
        right_column_layout.addWidget(create_metric_box("SUBTOTAL", "$ 4,000.00", "#5BC0DE"))
        right_column_layout.addWidget(create_metric_box("DESCUENTO", "$ 0.00", "#F0AD4E"))

        # Total Grande
        total_box = create_metric_box("TOTAL A PAGAR", "$ 4,000.00", "#2ECC71")
        total_box.setFixedSize(400, 120)
        total_box.findChild(QLabel, "").setFont(QFont("Arial", 24, QFont.Bold))  # Aumentar fuente del valor
        right_column_layout.addWidget(total_box)

        # 3. Botones de Acción
        action_button_style = "QPushButton { padding: 15px; border-radius: 8px; font-weight: bold; font-size: 11pt; color: white; }"

        btn_pay = QPushButton("PAGAR VENTA (F1)")
        btn_pay.setStyleSheet(action_button_style + "background-color: #007BFF;")

        btn_cancel = QPushButton("CANCELAR VENTA (Esc)")
        btn_cancel.setStyleSheet(action_button_style + "background-color: #E74C3C;")

        right_column_layout.addWidget(btn_pay)
        right_column_layout.addWidget(btn_cancel)
        right_column_layout.addStretch(1)

        main_h_layout.addWidget(right_column, 1)  # 1/3 del ancho

        self.content_area_layout.addWidget(main_sales_container)
        self.content_area_layout.addStretch(1)

    # ------------------------------------------------------------------
    # CONSTRUCCIÓN DEL DASHBOARD (Área Principal)
    # ------------------------------------------------------------------
    def _build_dashboard(self):
        """Construye la vista del dashboard con métricas, tabla y un slider de ejemplo."""
        datos_metricas = obtener_datos_dashboard_simulados()

        title_label = QLabel("PANEL DE CONTROL")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.content_area_layout.addWidget(title_label)

        # ... (Controles Rápidos y Grid de Métricas sin cambios) ...
        # --- SLIDER (Controles Rápidos) ---
        slider_frame = QFrame()
        slider_frame.setStyleSheet("background-color: #E6EAF0; border-radius: 8px; padding: 15px; margin-bottom: 10px;")
        slider_layout = QHBoxLayout(slider_frame)

        label_slider_title = QLabel("Umbral de Stock Mínimo (Valor: 5)")
        label_slider_title.setFont(QFont("Arial", 10, QFont.Bold))
        self.stock_value_label = label_slider_title

        self.stock_slider = QSlider(Qt.Horizontal)
        self.stock_slider.setRange(0, 20)
        self.stock_slider.setValue(5)
        self.stock_slider.setTickPosition(QSlider.TicksBelow)

        self.stock_slider.valueChanged.connect(self.update_stock_label)

        slider_layout.addWidget(label_slider_title)
        slider_layout.addWidget(self.stock_slider)

        self.content_area_layout.addWidget(slider_frame)

        # --- GRID DE MÉTRICAS ---
        metrics_container = QWidget()
        metrics_container.setStyleSheet("background-color: #F0F0F0; border-radius: 5px; padding: 10px;")

        metric_grid_layout = QGridLayout(metrics_container)
        metric_grid_layout.setHorizontalSpacing(15)
        metric_grid_layout.setVerticalSpacing(15)

        metric_list = [
            ("COP EN CAJA", datos_metricas["caja_actual"], "#5BC0DE"),
            ("COMPRAS DEL MES", datos_metricas["compras_mes"], "#E74C3C"),
            ("EN VENTAS DEL DÍA", datos_metricas["ventas_dia"], "#2ECC71"),
            ("INVERTIDO EN STOCK", datos_metricas["stock_invertido"], "#7B68EE"),

            ("PROVEEDORES", datos_metricas["proveedores"], "#5CB85C"),
            ("MARCAS", datos_metricas["marcas"], "#F39C12"),
            ("PROMOCIONES", "12.00", "#9B59B6"),
            ("PRODUCTOS REGISTRADOS", datos_metricas["productos_reg"], "#34495E"),

            ("ARTÍCULOS AGOTADOS", datos_metricas["articulos_agotados"], "#E74C3C"),
            ("VENCEN EN 30 DÍAS", datos_metricas["vencen_30_dias"], "#F39C12"),
            ("CLIENTES", datos_metricas["clientes"], "#3498DB"),
            ("CRÉDITOS Y PAGARÉS", datos_metricas["creditos_pagares"], "#9B59B6"),
        ]

        row, col = 0, 0
        for title, value, color in metric_list:
            metric_box = create_metric_box(title, value, color)
            metric_grid_layout.addWidget(metric_box, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.content_area_layout.addWidget(metrics_container)

        # --- TABLA DE PRODUCTOS ---
        table_title = QLabel("ÚLTIMOS PRODUCTOS")
        table_title.setFont(QFont("Arial", 12, QFont.Bold))
        table_title.setStyleSheet("margin-top: 20px; margin-bottom: 5px;")
        self.content_area_layout.addWidget(table_title)

        self.product_table = QTableWidget()
        self._setup_product_table(self.product_table)
        self.content_area_layout.addWidget(self.product_table)

        self.content_area_layout.addStretch(1)

    # ------------------------------------------------------------------
    # FUNCIÓN DE VISTA GENÉRICA (NUEVO)
    # ------------------------------------------------------------------
    def _build_generic_view(self, view_name):
        """Construye una vista simple para botones no implementados."""
        title_label = QLabel(f"Módulo: {view_name.upper()}")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.content_area_layout.addWidget(title_label)

        content_label = QLabel(f"Aquí se implementará la gestión completa de '{view_name}'.")
        content_label.setFont(QFont("Arial", 12))
        content_label.setStyleSheet("color: #666; margin-top: 20px;")
        self.content_area_layout.addWidget(content_label)

        self.content_area_layout.addStretch(1)

    def update_stock_label(self, value):
        """Actualiza el texto del QLabel con el valor actual del slider."""
        self.stock_value_label.setText(f"Umbral de Stock Mínimo (Valor: {value})")

    def _setup_product_table(self, table_widget):
        """Configura la tabla con encabezados y datos de ejemplo."""
        headers = ["Barras", "Producto", "Marca", "Stock", "Precio"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)

        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.setSelectionBehavior(QTableWidget.SelectRows)

        table_data = [
            ["04022343", "GALLETA OREO", "SALDIMINI", "5.00", "1.50"],
            ["99000000", "PARACETAMOL", "SONY", "10.00", "4.00"],
            ["26338747", "MOVIL ESP", "MOVIL", "1.00", "2300.00"],
            ["123456789", "COCA COLA", "COCA COLA", "10.00", "26.00"],
            ["99000067", "MOUSE ÓPTICO", "GENIUS", "1.00", "70.00"],
        ]

        table_widget.setRowCount(len(table_data))
        for i, row in enumerate(table_data):
            for j, item in enumerate(row):
                table_item = QTableWidgetItem(item)
                if headers[j] == "Stock":
                    try:
                        stock_value = float(item)
                        if stock_value <= 1.0:
                            table_item.setBackground(QColor(255, 100, 100))
                    except ValueError:
                        pass
                table_widget.setItem(i, j, table_item)

        table_widget.resizeColumnsToContents()
        table_widget.horizontalHeader().setStretchLastSection(True)

    def _setup_sales_detail_table(self, table_widget):
        """Configura la tabla de detalles de venta con menos columnas."""
        headers = ["Código", "Producto", "Cantidad", "Precio Unitario", "Subtotal"]
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)

        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.setSelectionBehavior(QTableWidget.SelectRows)

        # Datos de ejemplo para la venta
        table_data = [
            ["04022343", "GALLETA OREO", "2", "1.50", "3.00"],
            ["99000000", "PARACETAMOL 500mg", "10", "4.00", "40.00"],
            ["123456789", "COCA COLA 2L", "1", "26.00", "26.00"],
        ]

        table_widget.setRowCount(len(table_data))
        for i, row in enumerate(table_data):
            for j, item in enumerate(row):
                table_item = QTableWidgetItem(item)
                table_widget.setItem(i, j, table_item)

        table_widget.resizeColumnsToContents()
        table_widget.horizontalHeader().setStretchLastSection(True)


# ========================================================
# 4. PUNTO DE ENTRADA
# ========================================================
if __name__ == "__main__":
    # La aplicación espera encontrar los recursos en:
    # assets/images/apubyte.jpg
    # assets/icons/menu_toggle.png, assets/icons/home.png, etc.
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())
