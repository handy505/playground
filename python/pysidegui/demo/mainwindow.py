#!/usr/bin/env python3

# Copyright (c) 2010-2011, 2013 Algis Kabaila. All rights reserved.
# This work is made available under  the terms of the 
# Creative Commons Attribution-ShareAlike 3.0 license,
# http://creativecommons.org/licenses/by-sa/3.0/. 

# combine.py - combination of ShowGPL, About, Close scripts   
# The purpose of this version of program is to show implementation
# of most code in one file - all_in_1!. The Ui_MainWindow is eliminated
# and does not appear in the program.
     
import sys
import time
import platform
     
import PySide
     
from PySide.QtCore import QRect
from PySide.QtGui import *
     
__version__ = '3.1.5'

    
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(800, 480)
        self.setWindowTitle('PySide GUI')
        #self.setWindowFlags(PySide.QtCore.Qt.FramelessWindowHint)

        # home tabpage         
        self.wgHome = QWidget(self)
        gridLayout = QGridLayout(self.wgHome)
        self.label1 = QLabel('main page')
        gridLayout.addWidget(self.label1, 0, 0)
        self.lednum1 = QLCDNumber(numDigits=3)
        self.lednum1.display(12)
        gridLayout.addWidget(self.lednum1, 1, 0)

        
        # serial tabpage
        self.wgSerial = QWidget(self)
        gridLayout = QGridLayout(self.wgSerial)
        self.lb1 = QLabel('serial page')
        self.lb2 = QLabel('label 2')
        self.lb3 = QLabel('label 3')
        gridLayout.addWidget(self.lb1, 0, 0)
        gridLayout.addWidget(self.lb2, 1, 0)
        gridLayout.addWidget(self.lb3, 2, 0)
        

        # stacked widget
        self.sw = QStackedWidget(self)
        self.sw.addWidget(self.wgHome)
        self.sw.addWidget(self.wgSerial)
        self.setCentralWidget(self.sw)
        
        

        actionHome = QAction(self)
        actionHome.setIcon(QIcon("icon/Home-50.png"))
        actionHome.triggered.connect(
            lambda: self.sw.setCurrentWidget(self.wgHome))

        actionSerial = QAction(self)
        actionSerial.setIcon(QIcon("icon/Unicast-50.png"))
        actionSerial.triggered.connect(
            lambda: self.sw.setCurrentWidget(self.wgSerial))

        iconToolBar = self.addToolBar("iconBar.png")
        iconToolBar.setIconSize(PySide.QtCore.QSize(60, 60))
        iconToolBar.addAction(actionHome)
        iconToolBar.addAction(actionSerial)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())
