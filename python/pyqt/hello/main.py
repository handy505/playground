from PyQt5 import QtWidgets
from ui import Ui_MainWindow
import sys

from datetime import datetime

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setText('Hello World!')

        self.ui.pushButton.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        now = datetime.now()
        self.ui.label.setText(str(now))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
