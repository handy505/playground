import htmlPy
import os
from backendInterface import BackEnd

app = htmlPy.AppGUI(title=u"Sample application")
app.maximized = False
app.template_path = os.path.abspath(".")
app.static_path = os.path.abspath(".")

be = BackEnd()
be.app = app

app.bind(be)
app.template = ("index.html", {})
app.start()