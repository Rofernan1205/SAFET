from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QHBoxLayout, QWidget,
)
from PySide6.QtCore import Qt # Centrar
from PySide6.QtGui import QPixmap # Eventos

image_path = "assets/images/ApuByte.png"


def input_style():
    """Estilos para los campos de entrada"""
    return """
    QLineEdit {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 5px;
        padding: 6px;
        color: white;
    }
    QLineEdit:focus {
        border: 1px solid #58a6ff;
        outline: none;
    }
    """


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - SAFET")
        self.resize(450, 500)
        self.setMinimumSize(450, 500)

        # 🚀 PRÁCTICA RECOMENDADA: Define y asigna tus atributos aquí
        self.user_input = QLineEdit()
        self.pass_input = QLineEdit()

        # Usar un QWidget central para el layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout principal de la ventana (centrador)
        outer_layout = QVBoxLayout(main_widget)
        outer_layout.setAlignment(Qt.AlignCenter)

        # Contenedor central con ancho limitado
        container = QWidget()
        container.setObjectName("container_login")
        container.setMinimumWidth(400)
        container.setMinimumHeight(450)
        container.setStyleSheet("""
        QWidget#container_login {
            background-color: #0d1117;
            border: 3px solid #ffffff;
            border-radius: 10px;
            padding: 15px;
        }
        """)

        form_layout = QVBoxLayout(container)
        form_layout.setAlignment(Qt.AlignCenter)

        # Logo
        logo = QLabel()
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo.setText("🔒")
            logo.setStyleSheet("font-size: 40px;")
        logo.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(logo)

        # Título
        title = QLabel("SAFET")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title_login")
        title.setStyleSheet("""
                QWidget#title_login {
                    font-size: 20px;
                    font-family: sans-serif;
                    font-weight: bold;
                    color: white;
                    margin-bottom: 30px;
                }
                """)
        form_layout.addWidget(title)

        # Input usuario
        self.user_input.setPlaceholderText("Usuario")
        self.user_input.setStyleSheet(input_style())
        form_layout.addWidget(self.user_input)

        # Input contraseña
        self.pass_input.setPlaceholderText("Password")

        # Input contraseña + forgot
        pass_layout = QHBoxLayout()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet(input_style())

        forgot = QLabel("<a href='#'>Forgot password?</a>")
        forgot.setOpenExternalLinks(True)
        forgot.setStyleSheet("color: #58a6ff; font-size: 12px; margin-left: 8px;")

        pass_layout.addWidget(self.pass_input)
        pass_layout.addWidget(forgot)

        wrapper = QWidget()
        wrapper.setLayout(pass_layout)
        form_layout.addWidget(wrapper)

        # Botón login
        login_btn = QPushButton("Sign in")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
        """)
        login_btn.clicked.connect(self.login)
        form_layout.addWidget(login_btn)

        # Añadir contenedor centrado al layout externo
        outer_layout.addWidget(container, alignment=Qt.AlignCenter)

        # Fondo oscuro
        self.setStyleSheet("background-color: #0d1117;")

    def login(self):
        """Acción al presionar el botón de login"""
        usuario = self.user_input.text()
        password = self.pass_input.text()
        print(f"Usuario: {usuario}, Password: {password}")


if __name__ == "__main__":
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()