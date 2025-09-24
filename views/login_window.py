from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QHBoxLayout, QWidget, QDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

image_path = "assets/images/ApuByte.png"


def input_style():
    """Estilos para los campos de entrada"""
    return """
    QLineEdit {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 5px;
        padding: 6px;
        margin: 20px 10px 0px 10px;
        color: #f0f6fc;
        font-size: 14px;
        font-family:sans-serif ;
        font-weight: bold;
        letter-spacing: 1.5px;
    }
    QLineEdit:focus {
        border: 1px solid white;
        outline: none;
    }
    """


def button_style():
    """Estilos para los botones de la aplicacion"""
    return """
        QPushButton {
            background-color: #238636;
            color: white;
            font-size: 18px;
            font-family: sans-serif;
            font-weight: bold;
            padding: 8px;
            border-radius: 5px;
            margin: 10px 10px 0 10px;
        }
        QPushButton:hover {
            background-color: #2ea043;
            cursor: pointing-hand;
        }
    """


def link_button_style():
    """Estilos para el boton que funciona como enlace"""
    return """
        QPushButton {
            background: none;
            border: none;
            color: #58a6ff;
            font-size: 14px;
            font-family: sans-serif;
            margin: 0px 10px 0px 10px;
            text-decoration: none;
        }
        QPushButton:hover {
            color: #66b2ff;
            cursor: pointing-hand;
            text-decoration: underline;
        }
    """


class ForgotPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recuperar contraseña")
        self.setFixedSize(300, 150)
        self.setStyleSheet("background-color: #0d1117; color: white;")

        layout = QVBoxLayout(self)

        info_label = QLabel("Ingresa tu correo para recuperar la contraseña:")
        info_label.setStyleSheet("font-size: 14px; margin-bottom: 5px;")
        layout.addWidget(info_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo electrónico")
        self.email_input.setStyleSheet(input_style().replace("20px 10px 0px 10px", "0"))
        layout.addWidget(self.email_input)

        send_btn = QPushButton("Enviar")
        send_btn.setStyleSheet(button_style().replace("18px", "14px").replace("10px", "0"))
        layout.addWidget(send_btn)

        send_btn.clicked.connect(self.accept)


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - SAFET")
        self.resize(400, 500)
        self.setMinimumSize(400, 500)

        self.user_input = QLineEdit()
        self.pass_input = QLineEdit()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        outer_layout = QVBoxLayout(main_widget)
        outer_layout.setAlignment(Qt.AlignCenter)

        container = QWidget()
        container.setObjectName("container_login")
        container.setMinimumWidth(350)
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
                    font-size: 40px;
                    font-family:sans-serif ;
                    font-weight: bold;
                    color: white;
                    margin-bottom: 30px;
                    letter-spacing: -3px;
                }
                """)
        form_layout.addWidget(title)

        # Input usuario
        self.user_input.setPlaceholderText("Usuario")
        self.user_input.setStyleSheet(input_style())
        form_layout.addWidget(self.user_input)

        # Input contraseña
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet(input_style())
        form_layout.addWidget(self.pass_input)

        # Botón login
        login_btn = QPushButton("Iniciar sesión")
        login_btn.setStyleSheet(button_style())
        login_btn.clicked.connect(self.login)
        form_layout.addWidget(login_btn)

        # Botón de "Olvidaste tu contraseña"
        forgot_btn = QPushButton("¿Olvidaste tu contraseña?")
        forgot_btn.setStyleSheet(link_button_style())
        forgot_btn.clicked.connect(self.forgot_password_action)

        forgot_layout = QHBoxLayout()
        forgot_layout.addStretch()
        forgot_layout.addWidget(forgot_btn)

        form_layout.addLayout(forgot_layout)

        outer_layout.addWidget(container, alignment=Qt.AlignCenter)

        self.setStyleSheet("background-color: #0d1117;")

    def login(self):
        """Acción al presionar el botón de login"""
        usuario = self.user_input.text()
        password = self.pass_input.text()
        print(f"Usuario: {usuario}, Password: {password}")

    def forgot_password_action(self):
        """Muestra el diálogo de recuperación de contraseña."""
        forgot_dialog = ForgotPasswordDialog(self)
        if forgot_dialog.exec() == QDialog.Accepted:
            email = forgot_dialog.email_input.text()
            print(f"Solicitud de recuperación para: {email}")


if __name__ == "__main__":
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()
