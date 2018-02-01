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
        self.nodePage = self._initNodePage()
        self.workPage = self._initWorkPage()
        self.confPage = self._initConfPage()

        # stacked widget
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.homePage)
        self.stack.addWidget(self.nodePage)
        self.stack.addWidget(self.workPage)
        self.stack.addWidget(self.confPage)
        self.setCentralWidget(self.stack)
        
        homeAction = QAction(self)
        homeAction.setIcon(QIcon("icon/Home-50.png"))
        homeAction.triggered.connect(lambda: self.stack.setCurrentWidget(self.homePage))

        nodeAction = QAction(self)
        nodeAction.setIcon(QIcon("icon/Unicast-50.png"))
        nodeAction.triggered.connect(lambda: self.stack.setCurrentWidget(self.nodePage))

        workAction = QAction(self)
        workAction.setIcon(QIcon("icon/Work-50.png"))
        workAction.triggered.connect(lambda: self.stack.setCurrentWidget(self.workPage))

        confAction = QAction(self)
        confAction.setIcon(QIcon("icon/Settings-50.png"))
        confAction.triggered.connect(lambda: self.stack.setCurrentWidget(self.confPage))

        iconToolBar = self.addToolBar('title')
        iconToolBar.setIconSize(QSize(50, 50))
        iconToolBar.addAction(homeAction)
        iconToolBar.addAction(nodeAction)
        iconToolBar.addAction(workAction)
        iconToolBar.addAction(confAction)
 
    def _initConfPage(self):
        conf_edit = QTextEdit('here is a demo configuration string')
        conf_edit.setReadOnly(True)
        conf_edit2 = QTextEdit('here is a demo configuration string2')
        vbox = QVBoxLayout()
        vbox.addWidget(conf_edit)
        vbox.addWidget(conf_edit2)

        result = QWidget(self)
        result.setLayout(vbox)
        return result


    def ping(self, ip):
        cmd = 'sudo ping {} -c 3'.format(ip)
        result = os.popen(cmd).read()
        self.shell_edit.setText(result)


    def unlock_button(self):
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(True)
        self.shell_edit.clear()


    def _initWorkPage(self):
        self.shell_edit = QTextEdit()
        self.shell_edit.setReadOnly(True)
        self.btn1 = QPushButton('Ping Ablerex')
        self.btn1.clicked.connect(lambda :self.btn1.setEnabled(False))
        self.btn1.clicked.connect(lambda :self.btn2.setEnabled(False))
        self.btn1.clicked.connect(lambda :self.ping('www.ablerex.com.tw'))
        self.btn2 = QPushButton('Ping Other')
        self.btn2.clicked.connect(lambda :self.btn1.setEnabled(False))
        self.btn2.clicked.connect(lambda :self.btn2.setEnabled(False))
        self.btn2.clicked.connect(lambda :self.ping('8.8.8.8'))
        clear_button = QPushButton('Clear')
        clear_button.clicked.connect(self.unlock_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.shell_edit)
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.btn2)
        vbox.addWidget(clear_button)

        result = QWidget(self)
        result.setLayout(vbox)
        return result


    def _initNodePage(self):
        labels = [QLabel('label-{}'.format(i)) for i in range(10)]
        vbox0 = QVBoxLayout()
        [vbox0.addWidget(lb) for lb in labels]

        vbox1 = QVBoxLayout()
        vbox1.addWidget(QLabel())
        vbox1.addWidget(QLabel())
        vbox1.addWidget(QLabel())
        vbox1.addWidget(QLabel())
        vbox1.addWidget(QLabel())
        vbox1.addWidget(QLabel())
        vbox1.addWidget(QLabel())

        hbox = QHBoxLayout()
        hbox.addLayout(vbox0)
        hbox.addLayout(vbox1)

        result = QWidget(self)
        result.setLayout(hbox)
        return result


    def _initHomePage(self):
        tx_label = QLabel('rs485 tx label')
        rx_label = QLabel('rs485 rx label')
        node_summary_label = QLabel('rs485 nodes summary')
        serial_pipelines_label = QLabel('serial pipelnes label')
        database_label = QLabel('database')
        upload_pipelins_label = QLabel('upload pipelnes label')
        feedback_pipelins_label = QLabel('feedback pipelnes label')
        psid_label = QLabel('psid')
        upload_label = QLabel('upload')
        hearbeat_label = QLabel('hearbeat')
        system_time_label = QLabel('system time')
        watchdog_label = QLabel('watchdog')
        version_label = QLabel('version')
        version_label.setStyleSheet('QLabel {background-color : red; color : blue;}')

        vbox1 = QVBoxLayout()
        vbox1.addWidget(tx_label)
        vbox1.addWidget(rx_label)
        vbox1.addWidget(QLineEdit())
        vbox1.addWidget(node_summary_label)
        vbox1.addSpacerItem(QSpacerItem(10,10))

        vbox2 = QVBoxLayout()
        vbox2.addWidget(serial_pipelines_label)
        vbox2.addWidget(database_label)
        vbox2.addWidget(upload_pipelins_label)
        vbox2.addWidget(feedback_pipelins_label)
        vbox2.addWidget(psid_label)
        vbox2.addWidget(upload_label)

        gbox1 = QGroupBox('RS-485')
        gbox1.setLayout(vbox1)
        gbox2 = QGroupBox('Database')
        gbox2.setLayout(vbox2)

        rightvbox = QVBoxLayout()
        rightvbox.addWidget(hearbeat_label)
        rightvbox.addWidget(system_time_label)
        rightvbox.addWidget(watchdog_label)
        rightvbox.addWidget(version_label)
        rightvbox.addWidget(QLabel())
        rightvbox.addWidget(QLabel())
        rightvbox.addWidget(QLabel())
        rightvbox.addWidget(QLabel())
        rightvbox.addWidget(QLabel())

        hbox = QHBoxLayout()
        #hbox.addLayout(leftvbox)
        #hbox.addLayout(gbox)
        vbox = QVBoxLayout()
        vbox.addWidget(gbox1)
        vbox.addWidget(gbox2)
        hbox.addLayout(vbox)
        hbox.addLayout(rightvbox)

        result = QWidget(self)
        result.setLayout(hbox)
        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec_())
