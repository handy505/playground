from PyQt5 import QtWidgets                                                                                                                                     
from ui import Ui_MainWindow
import sys

from datetime import datetime



class Model(object):
    def __init__(self):
        self.observer = None 

        self.num = 0


    def increase_num(self):
        self.num += 1
        self.notify()


    def notify(self):
        if self.observer:
            self.observer.update(self)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setText('Hello World!')


    def update(self, subject):
        self.ui.label.setText(str(subject.num))



class Controller(object):
    def __init__(self):
        self.view = MainWindow()

        self.model = Model()
        self.model.observer = self.view

        self.view.ui.pushButton.clicked.connect(self.buttonClicked)
        self.view.show()

    def buttonClicked(self):
        #now = datetime.now()
        #self.view.ui.label.setText(str(now))
        
        self.model.increase_num()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    con = Controller()
    sys.exit(app.exec_())

