from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import generator

import sys
import re, os

class Okno(QMainWindow):
    def __init__(self, *args, **kwargs):
        #region Window and widgets
        #Window
        super(Okno, self).__init__(*args, *kwargs)
        self.setWindowTitle("Threshold Generator")
        self.setWindowIcon(QIcon('Icons/binary.png'))

        #Title
        titleText = QLabel()
        titleText.setText("Threshold Generator")
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

        #Registers
        titleRegistersText = QLabel()
        titleRegistersText.setText("Number of LFSR registers:")
        titleRegistersText.setFont(QFont('Lucida Console',12))

        self.registersNumSpin = QSpinBox()
        self.registersNumSpin.setRange(1, 11)
        self.registersNumSpin.setSingleStep(2)

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

        #Bits
        titleBitsText = QLabel()
        titleBitsText.setText("Number of bits to generate:")
        titleBitsText.setFont(QFont('Lucida Console',12))

        self.bitsNumSpin = QSpinBox()
        self.bitsNumSpin.setRange(1, 1000000)

        bitsButton = QPushButton()
        bitsButton.setFixedSize(40,40)
        bitsButton.setIcon(QIcon('Icons/folder.png'))
        bitsButton.clicked.connect(self.bitsFileClicked)

        titleBitsLayout = QHBoxLayout()
        titleBitsLayout.addWidget(titleBitsText)
        titleBitsLayout.addWidget(self.bitsNumSpin)
        titleBitsLayout.addWidget(bitsButton)
        titleBitsLayoutW = QWidget()
        titleBitsLayoutW.setLayout(titleBitsLayout)

        #Files windows
        self.registersFromFileButton = QFileDialog()
        self.registersFromFileButton.setNameFilter("Text Files (*.txt)")
        self.registersFromFileButton.hide()

        self.bitsFromFileButton = QFileDialog()
        self.bitsFromFileButton.setNameFilter("Text Files (*.txt)")
        self.bitsFromFileButton.hide()

        self.configFromFileButton = QFileDialog()
        self.configFromFileButton.setNameFilter("Text Files (*.txt)")
        self.configFromFileButton.hide()

        #Init type
        self.randomButton = QRadioButton("Random init")
        self.randomButton.setChecked(True)

        self.zerosButton = QRadioButton("000...0001")

        initButtonsLayout = QHBoxLayout()
        initButtonsLayout.addWidget(self.randomButton)
        initButtonsLayout.addWidget(self.zerosButton)
        initButtonsLayout.setAlignment(Qt.AlignHCenter)
        initButtonsLayoutW = QWidget()
        initButtonsLayoutW.setLayout(initButtonsLayout)

        #Load config file
        """configText = QLabel()
        configText.setText("Load config file")
        configText.setFont(QFont('Lucida Console',12))

        configButton = QPushButton()
        configButton.setFixedSize(40,40)
        configButton.setIcon(QIcon('Icons/folder.png'))
        configButton.clicked.connect(self.configFileClicked)

        configLayout = QHBoxLayout()
        configLayout.addWidget(configText)
        configLayout.addWidget(configButton)
        configLayoutW = QWidget()
        configLayoutW.setLayout(configLayout)"""

        configButton = QPushButton()
        configButton.setText("GENERATE FROM CONFIG FILE")
        configButton.setFont(QFont('Lucida Console',10))
        configButton.clicked.connect(self.configFileClicked)

        configLayout = QHBoxLayout()
        configLayout.addWidget(configButton)
        configLayoutW = QWidget()
        configLayoutW.setLayout(configLayout)

        #Buttons
        generateButton = QPushButton()
        generateButton.setText("GENERATE")
        generateButton.setFont(QFont('Lucida Console',10))
        generateButton.clicked.connect(self.generateClicked)

        generateLayout = QHBoxLayout()
        generateLayout.addWidget(generateButton)
        generateLayoutW = QWidget()
        generateLayoutW.setLayout(generateLayout)

        #Main layout
        main = QVBoxLayout()
        main.setAlignment(Qt.AlignCenter)
        main.addWidget(titleLayoutW)
        main.addWidget(titleRegistersLayoutW)
        main.addWidget(titleBitsLayoutW)
        main.addWidget(initButtonsLayoutW)
        main.addWidget(generateLayoutW)
        main.addWidget(configLayoutW)

        mainW = QWidget()
        mainW.setLayout(main)

        self.setCentralWidget(mainW)
        #endregion

    def initState(self):
        """Checks init type. Returns 1 if random init was chosen, 0 if 000...0001"""
        if self.randomButton.isChecked():
            return 1
        else:
            return 0

    def generateClicked(self, regSizes = None, regValues = None):
        """Handles generate button"""
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
                print(len(r))
                c.write(str(len(r))+' ')
            c.write('\n')

            for r in thresholdFunc.LFSRregs:
                for el in r:
                    c.write(str(el))
                c.write('\n')
            c.close

            output = thresholdFunc.thresholdFunction(self.bitsNumSpin.value())

            f = open(filenameOutput[0], "w")
            for i in output:
                f.write(str(i))
            f.close

    def registersFileClicked(self):
        """Loads message from file"""
        self.bitsFromFileButton.hide()
        self.configFromFileButton.hide()
        self.registersFromFileButton.show()

        if self.registersFromFileButton.exec():
            files = self.registersFromFileButton.selectedFiles()
            f = open(files[0], 'r')
            with f:
                data = f.read()
                self.registersNumSpin.setValue(int(data))

    def bitsFileClicked(self):
        """Loads key from file"""
        self.registersFromFileButton.hide()
        self.configFromFileButton.hide()
        self.bitsFromFileButton.show()

        if self.bitsFromFileButton.exec():
            files = self.bitsFromFileButton.selectedFiles()
            f = open(files[0], 'r')
            with f:
                data = f.read()
                self.bitsNumSpin.setValue(int(data))



    def configFileClicked(self):
        """Loads config file"""
        self.registersFromFileButton.hide()
        self.bitsFromFileButton.hide()
        self.configFromFileButton.show()

        if self.configFromFileButton.exec():
            files = self.configFromFileButton.selectedFiles()
            f = open(files[0], 'r')
            with f:
                data = f.readlines()
                self.registersNumSpin.setValue(int(data[0]))
                self.bitsNumSpin.setValue(int(data[1]))

                regSizes = data[2]
                regSizes = regSizes[:-2]
                regSizes = regSizes.split()

                regValues = []
                for i in range(int(data[0])):
                    temp = data[3+i]
                    temp = temp[:-1]
                    temp = list(temp)
                    temp2 = []
                    for el in temp:
                        el2 = int(el)
                        temp2.append(el2)
                    regValues.append(temp2)
                self.generateClicked(regSizes, regValues)

    def infoWindow(self):
        """Opens info window"""
        infoW = QMessageBox()
        infoW.setWindowTitle("Threshold Generator")
        infoW.setWindowIcon(QIcon('Icons/info.png'))
        infoW.setFont(QFont('Lucida Console'))
        f = open("info.txt", "r", encoding='utf8')
        text = f.read()
        infoW.setText(text)
        infoW.setWindowModality(Qt.ApplicationModal)
        infoW.exec_()

#App and window initialization
app = QApplication(sys.argv)

window = Okno()
window.setFixedSize(600, 400)
window.setStyleSheet("background-color: rgb(220,220,220);")
window.show()

app.exec_()

"""TODO: 
    - pasek statusu czy coś
    - nieparzysta liczba rejestrów
    - info
"""