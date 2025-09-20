from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from database.connection import SessionLocal
from services.role_service import RolServicio
from schemas.role_schema import RolCrear, RolActualizar, RolSalida

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAFET")
        self.setGeometry(800, 400, 400, 200)

        # Botón de prueba
        btn = QPushButton("Crear Rol")
        btn.clicked.connect(self.crear_rol)


        layout = QVBoxLayout()
        layout.addWidget(btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def crear_rol(self):
        with SessionLocal() as db:
            service = RolServicio(db)
            try:
                nuevo = service.crear_rol(RolCrear(nombre="PruebaUI"))
                QMessageBox.information(self, "Éxito", f"Rol creado: {nuevo.nombre}")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
