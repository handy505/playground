from PyQt5 import QtWidgets                                                                                                                                     
from ui import Ui_MainWindow
import sys

from datetime import datetime



class Model(object):
    def __init__(self):
        pass

    def func(self, data):
        #return data * 2
        pass


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setText('Hello World!')



class Controller(object):
    def __init__(self):
        self.view = MainWindow()

        self.model = Model()

        self.view.ui.pushButton.clicked.connect(self.buttonClicked)
        self.view.show()

    def buttonClicked(self):
        now = datetime.now()
        self.view.ui.label.setText(str(now))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    con = Controller()
    sys.exit(app.exec_())

