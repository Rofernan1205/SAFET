import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLabel, QFrame, QTableWidget, QTableWidgetItem, QHBoxLayout,
    QPushButton, QSizePolicy
)
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor
from PySide6.QtCore import Qt, QSize


# ========================================================
# 1. SIMULACIÓN DE LA CAPA DE DATOS (SQLAlchemy ORM)
# ========================================================

# ¡IMPORTANTE! Reemplaza esto con tus modelos y conexión reales
# from database.connection import Session, Caja, Proveedor, CategoriaProducto, Usuario, Producto, Venta

def obtener_datos_dashboard_simulados():
    """
    Función que simula la consulta a la base de datos (SQLAlchemy).
    En tu proyecto real, aquí usarías session.query(Modelo).count()
    """

    # --- SIMULACIÓN DE CÁLCULOS REALES ---
    # En un entorno real, la lógica sería:
    # session = Session()
    # total_cajas = session.query(Caja).filter(Caja.estado == "Abierta").count()
    # total_stock = session.query(func.sum(Producto.stock)).scalar()
    # ...
    # session.close()

    return {
        # Columna 1
        "caja_actual": "$ 84.00",
        "proveedores": "6.00",
        "articulos_agotados": "64.00",

        # Columna 2
        "compras_mes": "$ 1,494.21",
        "marcas": "19.00",
        "vencen_30_dias": "0.00",

        # Columna 3
        "ventas_dia": "$ 4.00",
        "promociones": "12.00",
        "clientes": "41.00",

        # Columna 4
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

    # Etiqueta para el Valor
    value_label = QLabel(value)
    value_label.setFont(QFont("Arial", 16, QFont.Bold))

    # Etiqueta para el Título
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

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Botón Principal (Header)
        self.header_button = self._create_header_button(title, icon_path)
        self.header_button.clicked.connect(self.toggle_collapse)
        self.main_layout.addWidget(self.header_button)

        # Contenedor del Submenú
        self.submenu_container = QWidget()
        self.submenu_layout = QVBoxLayout(self.submenu_container)
        self.submenu_layout.setContentsMargins(15, 0, 0, 0)  # Identación
        self.submenu_layout.setSpacing(0)

        # Llenar el submenú
        for item_text in submenu_items:
            sub_button = self._create_submenu_button(item_text)
            self.submenu_layout.addWidget(sub_button)

        self.submenu_container.hide()
        self.main_layout.addWidget(self.submenu_container)

    def _create_header_button(self, text, icon_path):
        """Crea el botón principal con estilo para el menú lateral."""
        btn = QPushButton(text)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(18, 18))

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
                background-color: #007BFF; /* Color de hover */
                color: white;
            }
        """)
        return btn

    def _create_submenu_button(self, text):
        """Crea el botón del submenú con indentación."""
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton { 
                text-align: left; 
                padding: 8px 10px 8px 35px; 
                background-color: #3C4B64; 
                border: none;
                color: #aaa; 
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #4C5A72;
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


def create_simple_menu_item(text, icon_path, is_selected=False):
    """Crea un ítem de menú simple que no se colapsa."""
    btn = QPushButton(text)
    btn.setIcon(QIcon(icon_path))
    btn.setIconSize(QSize(18, 18))

    style = """
        QPushButton { 
            text-align: left; 
            padding: 10px 10px 10px 5px; 
            border: none;
            font-size: 11pt;
        }
    """
    if is_selected:
        style += "QPushButton { background-color: #007BFF; color: white; }"
    else:
        style += "QPushButton { background-color: #2F3D55; color: #ccc; }"
        style += "QPushButton:hover { background-color: #3C4B64; color: white; }"

    btn.setStyleSheet(style)
    return btn


# ========================================================
# 3. VENTANA PRINCIPAL DE LA APLICACIÓN
# ========================================================

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAFET - Sistema de Ventas e Inventario")
        self.setGeometry(100, 100, 1300, 900)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout Principal: Horizontal (Sidebar | Contenido)
        self.main_h_layout = QHBoxLayout(main_widget)
        self.main_h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_h_layout.setSpacing(0)

        # 1. Crear y añadir la Barra Lateral
        self._build_sidebar()

        # 2. Crear el Área de Contenido
        self.content_area = QWidget()
        self.content_area_layout = QVBoxLayout(self.content_area)
        self.content_area_layout.setContentsMargins(15, 15, 15, 15)

        # Cargar el Dashboard al inicio
        self._build_dashboard()

        # 3. Ensamblar todo
        self.main_h_layout.addWidget(self.sidebar)
        self.main_h_layout.addWidget(self.content_area, 1)  # El 1 hace que tome el espacio restante

    def _build_sidebar(self):
        """Construye la barra lateral completa con usuario y menús desplegables."""
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(230)
        self.sidebar.setStyleSheet("background-color: #2F3D55;")

        self.sidebar_v_layout = QVBoxLayout(self.sidebar)
        self.sidebar_v_layout.setAlignment(Qt.AlignTop)
        self.sidebar_v_layout.setSpacing(0)
        self.sidebar_v_layout.setContentsMargins(0, 0, 0, 0)

        # --- Cabecera de Usuario ---
        user_header = QWidget()
        user_header.setStyleSheet("background-color: #243147; padding: 10px;")
        user_layout = QVBoxLayout(user_header)

        user_layout.addWidget(QLabel("ADMIN"), alignment=Qt.AlignCenter)
        user_layout.addWidget(QLabel("EMPLEADO"), alignment=Qt.AlignCenter)
        self.sidebar_v_layout.addWidget(user_header)

        # --- Menú Items ---

        # Ítem Inicio (Seleccionado)
        self.sidebar_v_layout.addWidget(create_simple_menu_item("Inicio", "icons/home.png", is_selected=True))

        # Ítem Desplegable: Almacén
        almacen_submenu = ["Categoría", "Presentacion", "Marca", "Producto", "Perecederos"]
        almacen_menu = CollapseMenu("Almacén", "icons/almacen.png", almacen_submenu)
        self.sidebar_v_layout.addWidget(almacen_menu)

        # Ítems Simples (resto del menú)
        self.sidebar_v_layout.addWidget(create_simple_menu_item("Cotizaciones", "icons/cotizaciones.png"))
        self.sidebar_v_layout.addWidget(create_simple_menu_item("Compras", "icons/compras.png"))
        self.sidebar_v_layout.addWidget(create_simple_menu_item("Caja", "icons/caja.png"))
        self.sidebar_v_layout.addWidget(create_simple_menu_item("Ventas", "icons/ventas.png"))
        self.sidebar_v_layout.addWidget(create_simple_menu_item("Inventario", "icons/inventario.png"))
        self.sidebar_v_layout.addWidget(create_simple_menu_item("Usuarios", "icons/usuario.png"))
        self.sidebar_v_layout.addWidget(create_simple_menu_item("Parametros", "icons/parametros.png"))

        self.sidebar_v_layout.addStretch(1)  # Empuja los elementos hacia arriba

    def _build_dashboard(self):
        """Construye la vista del dashboard con métricas y tabla."""

        # Limpiar el área de contenido (si viniera de otra vista)
        for i in reversed(range(self.content_area_layout.count())):
            widget = self.content_area_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        datos_metricas = obtener_datos_dashboard_simulados()  # <--- OBTENER DATOS REALES AQUÍ

        # Título General
        title_label = QLabel("PANEL DE CONTROL")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.content_area_layout.addWidget(title_label)

        # --- GRID DE MÉTRICAS ---
        metric_grid_layout = QGridLayout()
        metric_grid_layout.setHorizontalSpacing(15)
        metric_grid_layout.setVerticalSpacing(15)

        # Definir métricas con sus colores (simulando los 4 colores de cada fila)
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

        self.content_area_layout.addLayout(metric_grid_layout)

        # --- TABLA DE PRODUCTOS ---
        table_title = QLabel("ÚLTIMOS PRODUCTOS")
        table_title.setFont(QFont("Arial", 12, QFont.Bold))
        table_title.setStyleSheet("margin-top: 20px; margin-bottom: 5px;")
        self.content_area_layout.addWidget(table_title)

        self.product_table = QTableWidget()
        self._setup_product_table()
        self.content_area_layout.addWidget(self.product_table)

        # Ajustar para que el contenido no ocupe toda la altura si es pequeño
        self.content_area_layout.addStretch(1)

    def _setup_product_table(self):
        """Configura la tabla con encabezados y datos de ejemplo."""
        headers = ["Barras", "Producto", "Marca", "Stock", "Precio"]
        self.product_table.setColumnCount(len(headers))
        self.product_table.setHorizontalHeaderLabels(headers)

        self.product_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.product_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Datos de ejemplo para la tabla
        table_data = [
            ["04022343", "GALLETA OREO", "SALDIMINI", "5.00", "1.50"],
            ["99000000", "PARACETAMOL", "SONY", "10.00", "4.00"],
            ["26338747", "MOVIL ESP", "MOVIL", "1.00", "2300.00"],
            ["123456789", "COCA COLA", "COCA COLA", "10.00", "26.00"],
            ["99000067", "MOUSE ÓPTICO", "GENIUS", "1.00", "70.00"],
        ]

        self.product_table.setRowCount(len(table_data))
        for i, row in enumerate(table_data):
            for j, item in enumerate(row):
                table_item = QTableWidgetItem(item)
                # Ejemplo de color en el Stock (rojo para 1, verde para > 1)
                if headers[j] == "Stock":
                    try:
                        stock_value = float(item)
                        if stock_value <= 1.0:
                            table_item.setBackground(QColor(255, 100, 100))  # Rojo claro
                    except ValueError:
                        pass
                self.product_table.setItem(i, j, table_item)

        self.product_table.resizeColumnsToContents()
        self.product_table.horizontalHeader().setStretchLastSection(True)


# ========================================================
# 4. PUNTO DE ENTRADA
# ========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())