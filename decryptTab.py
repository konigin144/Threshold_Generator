from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5 import QtTest

import generator

import sys
import re, os
from bitarray import bitarray

class Decrypt(QWidget):
    def __init__(self, parent): 
        super(QWidget, self).__init__(parent)  

        #Title
        titleText = QLabel()
        titleText.setText("Decrypt")
        titleText.setAlignment(Qt.AlignHCenter)
        titleText.setFont(QFont('Lucida Console',30))

        titleButton = QPushButton()
        titleButton.setFixedSize(40,40)
        titleButton.setIcon(QIcon('Icons/info.png'))
        titleButton.clicked.connect(self.infoWindow)

        titleLayout = QHBoxLayout()
        titleLayout.addWidget(titleText)
        titleLayout.addWidget(titleButton)
        titleLayoutW = QWidget()
        titleLayoutW.setLayout(titleLayout)

        #Status
        self.statusText = QLabel()
        self.statusText.setText("Set parameters below or choose a config file")
        self.statusText.setAlignment(Qt.AlignCenter)
        self.statusText.setFont(QFont('Lucida Console',12))

        #File
        choosefileText = QLabel()
        choosefileText.setText("Choose file to decrypt:")
        choosefileText.setFont(QFont('Lucida Console',12))

        self.chooseFilePath = QLineEdit()
        self.chooseFilePath.setReadOnly(True)
        self.chooseFilePath.setText("")
        self.chooseFilePath.setAlignment(Qt.AlignCenter)
        self.chooseFilePath.setFont(QFont('Lucida Console',10))

        chooseFileButton = QPushButton()
        chooseFileButton.setFixedSize(40,40)
        chooseFileButton.setIcon(QIcon('Icons/folder.png'))
        chooseFileButton.clicked.connect(self.decryptFileClicked)

        chooseFileLayout = QHBoxLayout()
        chooseFileLayout.addWidget(choosefileText)
        chooseFileLayout.addWidget(self.chooseFilePath)
        chooseFileLayout.addWidget(chooseFileButton)
        chooseFileLayoutW = QWidget()
        chooseFileLayoutW.setLayout(chooseFileLayout)

        #Key
        chooseKeyText = QLabel()
        chooseKeyText.setText("Choose file with key:")
        chooseKeyText.setFont(QFont('Lucida Console',12))

        self.chooseKeyPath = QLineEdit()
        self.chooseKeyPath.setReadOnly(True)
        self.chooseKeyPath.setText("")
        self.chooseKeyPath.setAlignment(Qt.AlignCenter)
        self.chooseKeyPath.setFont(QFont('Lucida Console',10))

        chooseKeyButton = QPushButton()
        chooseKeyButton.setFixedSize(40,40)
        chooseKeyButton.setIcon(QIcon('Icons/folder.png'))
        chooseKeyButton.clicked.connect(self.keyFileClicked)

        chooseKeyLayout = QHBoxLayout()
        chooseKeyLayout.addWidget(chooseKeyText)
        chooseKeyLayout.addWidget(self.chooseKeyPath)
        chooseKeyLayout.addWidget(chooseKeyButton)
        chooseKeyLayoutW = QWidget()
        chooseKeyLayoutW.setLayout(chooseKeyLayout)

        #File windows
        self.configFromFileButton = QFileDialog()
        self.configFromFileButton.setNameFilter("Text Files (*.txt)")
        self.configFromFileButton.hide()

        self.decryptFileButton = QFileDialog()
        self.decryptFileButton.setNameFilter("Text Files (*.txt)")
        self.decryptFileButton.hide()

        #Decrypt button
        decryptButton = QPushButton()
        decryptButton.setText("DECRYPT")
        decryptButton.setFont(QFont('Lucida Console',10))
        decryptButton.clicked.connect(self.decryptClicked)

        #Layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(titleLayoutW)
        self.layout.addWidget(self.statusText)
        self.layout.addWidget(chooseFileLayoutW)
        self.layout.addWidget(chooseKeyLayoutW)
        self.layout.addWidget(decryptButton)
        self.setLayout(self.layout)

    def generateClicked(self, regSizes = None, regValues = None):
        """Handles generate button"""
        if regSizes is not False:
            for size in regSizes:
                if int(size) not in generator.ThresholdFunction.xorTable:
                    self.statusText.setStyleSheet('color: red')
                    self.statusText.setText("Wrong register size")
                    QtTest.QTest.qWait(3000)
                    self.statusText.setStyleSheet('color: black')
                    self.statusText.setText("Set parameters above or choose a config file")
                    return
            if len(regSizes) > 11:
                self.statusText.setStyleSheet('color: red')
                self.statusText.setText("Too many register (maximum is 11)")
                QtTest.QTest.qWait(3000)
                self.statusText.setStyleSheet('color: black')
                self.statusText.setText("Set parameters above or choose a config file")
                return
            if len(regSizes) < 1:
                self.statusText.setStyleSheet('color: red')
                self.statusText.setText("Number of registers cannot be lower than 1")
                QtTest.QTest.qWait(3000)
                self.statusText.setStyleSheet('color: black')
                self.statusText.setText("Set parameters above or choose a config file")
                return
            if len(regSizes) %2 == 0:
                self.statusText.setStyleSheet('color: red')
                self.statusText.setText("Number of registers should be odd")
                QtTest.QTest.qWait(3000)
                self.statusText.setStyleSheet('color: black')
                self.statusText.setText("Set parameters above or choose a config file")
                return
        self.statusText.setStyleSheet('color: blue')
        self.statusText.setText("Processing...")
        thresholdFunc = generator.ThresholdFunction(self.registersNumSpin.value(), self.initState(), regValues)
        filenameOutput = QFileDialog.getSaveFileName(self, "Open Text File", os.path.abspath(os.getcwd()), "Text Files (*.txt)")
        
        if filenameOutput[0] != '':
            dir = filenameOutput[0]
            i = len(dir)-1
            while True:
                dir = dir[:-1]
                i-=1
                if dir[i] == '.':
                    dir = dir[:-1]
                    break
            dir += '_config.txt'
            c = open(dir, "w")
            c.write(str(self.registersNumSpin.value())+'\n')
            c.write(str(self.bitsNumSpin.value())+'\n')
            for r in thresholdFunc.LFSRregs:
                c.write(str(len(r))+' ')
            c.write('\n')

            for r in thresholdFunc.LFSRregs:
                for el in r:
                    c.write(str(el))
                c.write('\n')
            c.close

            output = thresholdFunc.thresFunc(self.bitsNumSpin.value())

            f = open(filenameOutput[0], "w")
            for i in output:
                f.write(str(i))
            f.close

            self.statusText.setStyleSheet('color: green')
            self.statusText.setText("The result and config files has been created")
            QtTest.QTest.qWait(3000)
        self.statusText.setStyleSheet('color: black')
        self.statusText.setText("Set parameters above or choose a config file")

    def keyFileClicked(self):
        """Sets file path"""
        self.configFromFileButton.hide()
        self.decryptFileButton.show()

        if self.decryptFileButton.exec():
            files = self.decryptFileButton.selectedFiles()
            self.chooseKeyPath.setText(files[0])            

    def decryptFileClicked(self):
        """Sets file path"""
        self.configFromFileButton.hide()
        self.decryptFileButton.show()

        if self.decryptFileButton.exec():
            files = self.decryptFileButton.selectedFiles()
            self.chooseFilePath.setText(files[0])            

    def decryptClicked(self):
        """Decrypts file"""
        f = open(self.chooseFilePath.text(), 'r')
        with f:
            data = f.read()
            f.close()
        f = open(self.chooseKeyPath.text(), 'r')
        with f:
            key = f.read()
            f.close()
        
        if len(key) >= len(data):

            result = []
            for i in range(len(data)):
                result.append(int(data[i]) ^ int(key[i]))
            result = bitarray(result).tobytes().decode('utf-8')
            filenameOutput = QFileDialog.getSaveFileName(self, "Open Text File", os.path.abspath(os.getcwd()), "Text Files (*.txt)")
            if filenameOutput[0] != '':
                f = open(filenameOutput[0], "w")
                f.write(result)
                f.close

    def infoWindow(self):
        """Opens info window"""
        infoW = QMessageBox()
        infoW.setWindowTitle("Decryptor")
        infoW.setWindowIcon(QIcon('Icons/info.png'))
        #infoW.setFont(QFont('Lucida Console'))
        #infoW.setStyleSheet("QLabel{min-width: 900px;}")
        f = open("info3.txt", "r", encoding='utf8')
        text = f.read()
        infoW.setText(text)
        infoW.setWindowModality(Qt.ApplicationModal)
        infoW.exec_()