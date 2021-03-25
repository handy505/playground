#!/usr/bin/env python3
     
import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *
    
class DemoWindow(QWidget):
    def __init__(self, parent=None):
        super(DemoWindow, self).__init__(parent)
        x, y, w, h = 0, 0, 800, 480
        self.setGeometry(x, y, w, h)

        vbox = QVBoxLayout(self)

        self.lb = QLabel('123', self)
        vbox.addWidget(self.lb)

        btn = QPushButton('btn', self)
        btn.clicked.connect(self.click)
        vbox.addWidget(btn)

        self.setLayout(vbox)

    def click(self):
        print('clicked')
        self.lb.setText(str(time.time()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DemoWindow()
    win.show()
    sys.exit(app.exec_())
