from PyQt5 import QtWidgets                                                                                                                                     
from ui import Ui_MainWindow
import sys

from datetime import datetime
import time

import threading


class Model(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)       
        self.observer = None 
        self.num = 0


    def add_observer(self, arg):
        self.observer = arg


    def notify(self):
        if self.observer:
            self.observer.update(self)


    def run(self):
        while True:
            self.num += 1
            self.notify()
            time.sleep(1)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setText('Hello World!')


    def update(self, subject):
        s = str(subject.num)
        self.ui.label.setText(s)



'''class Controller(object):
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
        '''
        


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    #con = Controller()

    view = MainWindow()

    model = Model()
    model.add_observer(view)
    model.start()

    view.show()

    sys.exit(app.exec_())

