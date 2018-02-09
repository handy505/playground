#!/usr/bin/env python3
     
import os
import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *
    

class DemoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DemoWindow, self).__init__(parent)
        self.resize(800, 480)
        self.setWindowTitle('PySide Demo')

        self.homePage = self._initHomePage()

        # stacked widget
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.homePage)
        self.setCentralWidget(self.stack)
        
        homeAction = QAction(self)
        homeAction.setIcon(QIcon("icon/Home-50.png"))
        homeAction.triggered.connect(lambda: self.stack.setCurrentWidget(self.homePage))

        iconToolBar = self.addToolBar('title')
        iconToolBar.setIconSize(QSize(80, 60))
        iconToolBar.addAction(homeAction)


    def _initHomePage(self):
        self.edit = QTextEdit()
        self.input1 = QLineEdit()
        self.excute1 = QPushButton('excute')
        self.input2 = QLineEdit()
        self.excute2 = QPushButton('excute')

        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.input1)
        hbox1.addWidget(self.excute1)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.input2)
        hbox2.addWidget(self.excute2)

        vbox = QVBoxLayout()
        vbox.addWidget(self.edit)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        result = QWidget(self)
        result.setLayout(vbox)
        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec_())
