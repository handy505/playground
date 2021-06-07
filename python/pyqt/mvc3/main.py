from PyQt5 import QtWidgets                                                                                                                                     
from ui import Ui_MainWindow
import sys

from datetime import datetime
import threading
import time



class Model(threading.Thread):
    def __init__(self):
        super().__init__()
        self.observer = None 

        self.num = 0
        self.now = datetime.now()


    def increase_num(self):
        self.num += 1
        self.notify()


    def notify(self):
        if self.observer:
            self.observer.update(self)

    def run(self):
        while True:

            self.now = datetime.now()
            self.notify()
            time.sleep(1)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setText('Hello World!')


    def update(self, subject):
        self.ui.label.setText(str(subject.num))
        self.ui.label_2.setText(str(subject.now))



class Controller(object):
    def __init__(self):
        self.view = MainWindow()

        self.model = Model()
        self.model.observer = self.view
        self.model.start()

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

