from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5 import QtTest

import generator, thresholdTab, encryptTab, decryptTab

import sys
import re, os
from bitarray import bitarray

class Okno(QMainWindow):
    def __init__(self, *args, **kwargs):       
        super(Okno, self).__init__(*args, *kwargs)
        self.setWindowTitle("Threshold Generator")
        self.setWindowIcon(QIcon('Icons/binary.png'))
 
        self.tabs = QTabWidget()
        self.tab1 = thresholdTab.Threshold(self)
        self.tab2 = encryptTab.Encrypt(self)
        self.tab3 = decryptTab.Decrypt(self)
        self.tabs.addTab(self.tab1, "Threshold Generator")
        self.tabs.addTab(self.tab2, "Encrypt")
        self.tabs.addTab(self.tab3, "Decrypt")

        self.setCentralWidget(self.tabs)

#App and window initialization
app = QApplication(sys.argv)

window = Okno()
window.setFixedSize(600, 400)
window.setStyleSheet("background-color: rgb(220,220,220);")
window.show()

app.exec_()