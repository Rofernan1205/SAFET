# Color principal
GRADIENT_GLOBAL = """
    background-color : #151a21;
    
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