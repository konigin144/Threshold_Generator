from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5 import QtTest

import generator

import sys
import re, os
from bitarray import bitarray

class Encrypt(QWidget):
    def __init__(self, parent): 
        super(QWidget, self).__init__(parent)  

        #Title
        titleText = QLabel()
        titleText.setText("Encrypt")
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
        self.statusText.setText("Set parameters below or choose a file with key")
        self.statusText.setAlignment(Qt.AlignCenter)
        self.statusText.setFont(QFont('Lucida Console',12))

        #Registers
        titleRegistersText = QLabel()
        titleRegistersText.setText("Number of LFSR registers:")
        titleRegistersText.setFont(QFont('Lucida Console',12))

        self.registersNumSpin = QSpinBox()
        self.registersNumSpin.setRange(1, 11)
        self.registersNumSpin.setSingleStep(2)
        self.registersNumSpin.lineEdit().setReadOnly(True)

        registersButton = QPushButton()
        registersButton.setFixedSize(40,40)
        registersButton.setIcon(QIcon('Icons/folder.png'))
        registersButton.clicked.connect(self.registersFileClicked)

        titleRegistersLayout = QHBoxLayout()
        titleRegistersLayout.addWidget(titleRegistersText)
        titleRegistersLayout.addWidget(self.registersNumSpin)
        titleRegistersLayout.addWidget(registersButton)
        titleRegistersLayoutW = QWidget()
        titleRegistersLayoutW.setLayout(titleRegistersLayout)

        #Init type
        self.randomButton = QRadioButton("Random init")
        self.randomButton.setChecked(True)

        self.zerosButton = QRadioButton("000...0001 init")

        initButtonsLayout = QHBoxLayout()
        initButtonsLayout.addWidget(self.randomButton)
        initButtonsLayout.addWidget(self.zerosButton)
        initButtonsLayout.setAlignment(Qt.AlignHCenter)
        initButtonsLayoutW = QWidget()
        initButtonsLayoutW.setLayout(initButtonsLayout)

        #File
        choosefileText = QLabel()
        choosefileText.setText("Choose file to encrypt:")
        choosefileText.setFont(QFont('Lucida Console',12))

        self.chooseFilePath = QLineEdit()
        self.chooseFilePath.setReadOnly(True)
        self.chooseFilePath.setText("")
        self.chooseFilePath.setAlignment(Qt.AlignCenter)
        self.chooseFilePath.setFont(QFont('Lucida Console',10))

        chooseFileButton = QPushButton()
        chooseFileButton.setFixedSize(40,40)
        chooseFileButton.setIcon(QIcon('Icons/folder.png'))
        chooseFileButton.clicked.connect(self.encyptFileClicked)

        chooseFileLayout = QHBoxLayout()
        chooseFileLayout.addWidget(choosefileText)
        chooseFileLayout.addWidget(self.chooseFilePath)
        chooseFileLayout.addWidget(chooseFileButton)
        chooseFileLayoutW = QWidget()
        chooseFileLayoutW.setLayout(chooseFileLayout)

        #File windows
        self.registersFromFileButton = QFileDialog()
        self.registersFromFileButton.setNameFilter("Text Files (*.txt)")
        self.registersFromFileButton.hide()

        self.keyFileButton = QFileDialog()
        self.keyFileButton.setNameFilter("Text Files (*.txt)")
        self.keyFileButton.hide()

        self.encryptFileButton = QFileDialog()
        self.encryptFileButton.setNameFilter("Text Files (*.txt)")
        self.encryptFileButton.hide()

        #Encrypt button
        encryptButton = QPushButton()
        encryptButton.setText("ENCRYPT")
        encryptButton.setFont(QFont('Lucida Console',10))
        encryptButton.clicked.connect(self.encryptClicked)

        #Encrypt with key button
        encryptKeyButton = QPushButton()
        encryptKeyButton.setText("ENCRYPT WITH KEY")
        encryptKeyButton.setFont(QFont('Lucida Console',10))
        encryptKeyButton.clicked.connect(self.encryptKeyClicked)

        #Layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(titleLayoutW)
        self.layout.addWidget(self.statusText)
        self.layout.addWidget(titleRegistersLayoutW)
        self.layout.addWidget(initButtonsLayoutW)
        self.layout.addWidget(chooseFileLayoutW)
        self.layout.addWidget(encryptButton)
        self.layout.addWidget(encryptKeyButton)
        self.setLayout(self.layout)

    def initState(self):
        """Checks init type. Returns 1 if random init was chosen, 0 if 000...0001"""
        if self.randomButton.isChecked():
            return 1
        else:
            return 0

    def registersFileClicked(self):
        """Loads message from file"""
        self.keyFileButton.hide()
        self.registersFromFileButton.show()

        if self.registersFromFileButton.exec():
            files = self.registersFromFileButton.selectedFiles()
            f = open(files[0], 'r')
            with f:
                data = f.read()

                if int(data) > 11:
                    self.statusText.setStyleSheet('color: red')
                    self.statusText.setText("Too many register (maximum is 11)")
                    QtTest.QTest.qWait(3000)
                    self.statusText.setStyleSheet('color: black')
                    self.statusText.setText("Set parameters above or choose a config file")
                    return
                elif int(data) < 1:
                    self.statusText.setStyleSheet('color: red')
                    self.statusText.setText("Number of registers cannot be lower than 1")
                    QtTest.QTest.qWait(3000)
                    self.statusText.setStyleSheet('color: black')
                    self.statusText.setText("Set parameters above or choose a config file")
                    return
                elif int(data)  %2 == 0:
                    self.statusText.setStyleSheet('color: red')
                    self.statusText.setText("Number of registers should be odd")
                    QtTest.QTest.qWait(3000)
                    self.statusText.setStyleSheet('color: black')
                    self.statusText.setText("Set parameters above or choose a config file")
                    return
                
                else:
                    self.registersNumSpin.setValue(int(data))
    
    def encyptFileClicked(self):
        """Sets file path"""
        self.keyFileButton.hide()
        self.registersFromFileButton.hide()
        self.encryptFileButton.show()

        if self.encryptFileButton.exec():
            files = self.encryptFileButton.selectedFiles()
            self.chooseFilePath.setText(files[0])            

    def encryptClicked(self, regSizes = None, regValues = None):
        f = open(self.chooseFilePath.text(), 'r')
        with f:
            data = f.read()
            f.close()
        bits = bitarray()
        bits.frombytes(data.encode('utf-8'))
        bits = bits.to01()
        
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
            # config file
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
            c.write(str(len(bits))+'\n')
            for r in thresholdFunc.LFSRregs:
                c.write(str(len(r))+' ')
            c.write('\n')

            for r in thresholdFunc.LFSRregs:
                for el in r:
                    c.write(str(el))
                c.write('\n')
            c.close

            #key
            dir2 = filenameOutput[0]
            i = len(dir2)-1
            while True:
                dir2 = dir2[:-1]
                i-=1
                if dir2[i] == '.':
                    dir2 = dir2[:-1]
                    break
            dir2 += '_key.txt'

            key = thresholdFunc.thresFunc(len(bits))

            f = open(dir2, "w")
            for i in key:
                f.write(str(i))
            f.close
            
            #result
            f = open(filenameOutput[0], "w")
            for i in range(len(bits)):
                el = int(bits[i]) ^ int(key[i])
                f.write(str(el))
            f.close

            self.statusText.setStyleSheet('color: green')
            self.statusText.setText("The result and config files has been created")
            QtTest.QTest.qWait(3000)
        self.statusText.setStyleSheet('color: black')
        self.statusText.setText("Set parameters above or choose a config file")

    def encryptKeyClicked(self):
        """Encrypts with key loaded from file"""
        self.registersFromFileButton.hide()
        self.keyFileButton.show()

        f = open(self.chooseFilePath.text(), 'r')
        with f:
            data = f.read()
            f.close()
        bits = bitarray()
        bits.frombytes(data.encode('utf-8'))
        bits = bits.to01()

        if self.keyFileButton.exec():
            files = self.keyFileButton.selectedFiles()
            f = open(files[0], 'r')
            with f:
                key = f.read()
                f.close()
            if len(key) >= len(bits):
                filenameOutput = QFileDialog.getSaveFileName(self, "Open Text File", os.path.abspath(os.getcwd()), "Text Files (*.txt)")        
                if filenameOutput[0] != '':
                    f = open(filenameOutput[0], "w")
                    for i in range(len(bits)):
                        el = int(bits[i]) ^ int(key[i])
                        f.write(str(el))
                    f.close
            else:
                self.statusText.setStyleSheet('color: red')
                self.statusText.setText("Key is too short (minimum "+str(len(bits))+")")
                QtTest.QTest.qWait(3000)
                self.statusText.setStyleSheet('color: black')
                self.statusText.setText("Set parameters above or choose a config file")
                return

    def infoWindow(self):
        """Opens info window"""
        infoW = QMessageBox()
        infoW.setWindowTitle("Encryptor")
        infoW.setWindowIcon(QIcon('Icons/info.png'))
        #infoW.setFont(QFont('Lucida Console'))
        #infoW.setStyleSheet("QLabel{min-width: 900px;}")
        f = open("info2.txt", "r", encoding='utf8')
        text = f.read()
        infoW.setText(text)
        infoW.setWindowModality(Qt.ApplicationModal)
        infoW.exec_()