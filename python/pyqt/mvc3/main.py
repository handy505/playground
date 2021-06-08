from PyQt5 import QtWidgets                                                                                                                                     
from ui import Ui_MainWindow
import sys

import datetime
import threading
import time


class Model(threading.Thread):
    def __init__(self):
        super().__init__()
        self.observer = None 
        self.now = datetime.datetime.now()
        self.alarmtime = None
        self.countdown = None


    def notify(self):
        if self.observer:
            self.observer.update(self)


    def set_alarm_time(self, hour, minute):
        self.alarmtime = datetime.time(hour=hour, minute=minute)
        self.notify()


    def update_countdown(self):
        if self.alarmtime:
            alarmdt = datetime.datetime.combine(datetime.date.today(), self.alarmtime)
            self.countdown = alarmdt - self.now


    def run(self):
        while True:
            self.now = datetime.datetime.now()
            self.update_countdown()
            self.notify()
            time.sleep(1)


# ---------------------------------------------------------------
# viewer
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setText('Hello World!')


    def update(self, subject):
        self.ui.label.setText(str(subject.now))

        alarmtime = str(subject.alarmtime)
        self.ui.label_2.setText(alarmtime)

        countdown = str(subject.countdown)
        self.ui.label_3.setText(countdown)


# ---------------------------------------------------------------
class Controller(object):
    def __init__(self):
        self.view = MainWindow()

        self.model = Model()
        self.model.observer = self.view
        self.model.start()

        self.view.ui.setButton.clicked.connect(self.setAlarmTime)
        self.view.ui.clearButton.clicked.connect(self.clearAlarmTime)
        self.view.show()


    def setAlarmTime(self):
        hour = self.view.ui.timeEdit.time().hour()
        minute = self.view.ui.timeEdit.time().minute()
        self.model.set_alarm_time(hour, minute)


    def clearAlarmTime(self):
        self.model.alarmtime = None
        self.model.countdown = None
        self.view.ui.label_2.clear()
        self.view.ui.label_3.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    con = Controller()
    sys.exit(app.exec_())

