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
import random
from PySide.QtCore import *
from PySide.QtGui import *
     
__version__ = '3.1.5'

    
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(800, 480)
        self.setWindowTitle('PySide GUI')
        #self.setWindowFlags(PySide.QtCore.Qt.FramelessWindowHint)

        # home tabpage         
        self.homePage = QWidget(self)
        self.label1 = QLabel('main page')
        self.lednum1 = QLCDNumber(numDigits=10)
        self.lednum1.setSegmentStyle(QLCDNumber.Flat)
        #self.lednum1.display(123)
        self.lednum1.display('Solar')
        self.lednum1.resize(100, 100)
        self.incButton = QPushButton('Inc')
        self.decButton = QPushButton('Dec')
        self.rndButton = QPushButton('Random')


        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.label1)
        hbox0.addWidget(self.lednum1)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.incButton)
        hbox1.addWidget(self.decButton)
        hbox1.addWidget(self.rndButton)

        vbox = QVBoxLayout(self.homePage)
        vbox.addStretch(1)
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)

        self.homePage.setLayout(vbox)
    

        
        # serial tabpage
        self.machinePage = QWidget(self)
        grid = QGridLayout(self.machinePage)
        grid.addWidget(QLabel('Alarm'), 0, 0, Qt.AlignRight)
        grid.addWidget(QLabel('Error'), 0, 2, Qt.AlignRight)
        grid.addWidget(QLabel('Output Power(KW)'), 1, 0, Qt.AlignRight)
        grid.addWidget(QLabel('Total Output Power(KWH)'), 1, 2, Qt.AlignRight)

        for r in range(0, 7):
            num = QLCDNumber(numDigits=6)
            grid.addWidget(num, r, 1)
        
        for r in range(0, 6):
            num = QLCDNumber(numDigits=6)
            grid.addWidget(num, r, 3)

        # stacked widget
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.homePage)
        self.stack.addWidget(self.machinePage)
        self.setCentralWidget(self.stack)
        
        

        self.incButton.clicked.connect(
            lambda: self.lednum1.display(self.lednum1.value() + 1))
        self.decButton.clicked.connect(
            lambda: self.lednum1.display(self.lednum1.value() - 1))
        self.rndButton.clicked.connect(
            lambda: self.lednum1.display(random.randint(0,100)))

        actionHome = QAction(self)
        actionHome.setIcon(QIcon("icon/Home-50.png"))
        actionHome.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.homePage))

        actionSerial = QAction(self)
        actionSerial.setIcon(QIcon("icon/Unicast-50.png"))
        actionSerial.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.machinePage))

        iconToolBar = self.addToolBar("iconBar.png")
        iconToolBar.setIconSize(QSize(80, 60))
        iconToolBar.addAction(actionHome)
        iconToolBar.addAction(actionSerial)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    sys.exit(app.exec_())
