from PySide6.QtWidgets import QApplication, QWidget, QMessageBox

def center_on_screen(widget: QWidget):
    """Centra un widget en la pantalla principal."""
    screen = QApplication.primaryScreen().geometry()
    size = widget.geometry()
    x = (screen.width() - size.width()) // 2
    y = (screen.height() - size.height()) // 2
    widget.move(x, y)

