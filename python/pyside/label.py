#!/usr/bin/env python3
     
import sys
from PySide.QtCore import *
from PySide.QtGui import *
    
class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.msgLabel = QLabel('abcdefg', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWidget()
    win.show()
    sys.exit(app.exec_())
