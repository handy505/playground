import os
import htmlPy
from PyQt4 import QtGui
import PySide
from back_end_codes.backendInterface import BackEnd


# Initial confiurations
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# GUI initializations
app = htmlPy.AppGUI(title=u"Application", maximized=False, plugins=True)


# GUI configurations
app.static_path = os.path.join(BASE_DIR, "static/")
app.template_path = os.path.join(BASE_DIR, "templates/")

app.web_app.setMinimumWidth(800)
app.web_app.setMinimumHeight(480)
app.window.setWindowIcon(PySide.QtGui.QIcon(BASE_DIR + "./img/icon.png"))

app.template = ("index.html", {"username": "htmlPy_user"})
# Binding of back-end functionalities with GUI

# Import back-end functionalities
#from html_to_python import ClassName

# Register back-end functionalities
#app.bind(ClassName())

be = BackEnd()
be.app = app

app.bind(be)

# Instructions for running application
if __name__ == "__main__":
    
    # The driver file will have to be imported everywhere in back-end.
    # So, always keep app.start() in if __name__ == "__main__" conditional
    app.start()