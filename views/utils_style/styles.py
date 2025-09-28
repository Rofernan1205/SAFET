# Color principal
GRADIENT_GLOBAL = """
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0.0  #000000,
        stop:0.1  #1e1e1e,
        stop:0.2  #363535,
        stop:0.3  #4f4e4e,
        stop:0.4  #6a6969,
        stop:0.6  #6a6969,
        stop:0.7  #4f4e4e,
        stop:0.8  #363535,
        stop:0.9  #1e1e1e,
        stop:1.0  #000000
    );
"""
# Estilos para los botones de la aplicacion
BUTTON_STYLE ="""
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
        }
"""
# Estilos para input
INPUT_STYLE =  """
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
        border: 1px solid #409eff;
        outline: none;
    }
    """

# Estilos para el boton que funciona como enlace
LINK_BUTTON =  """
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
            text-decoration: underline;
        }
    """