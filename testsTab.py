from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5 import QtTest

import generator

import sys
import re, os
from bitarray import bitarray

class Tests(QWidget):
    def __init__(self, parent): 
        super(QWidget, self).__init__(parent)  

        #Title
        titleText = QLabel()
        titleText.setText("Tests")
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
        self.statusText.setText("Choose file and test")
        self.statusText.setAlignment(Qt.AlignCenter)
        self.statusText.setFont(QFont('Lucida Console',12))

        #File
        choosefileText = QLabel()
        choosefileText.setText("Choose file to test")
        choosefileText.setFont(QFont('Lucida Console',12))

        self.chooseFilePath = QLineEdit()
        self.chooseFilePath.setReadOnly(True)
        self.chooseFilePath.setText("")
        self.chooseFilePath.setAlignment(Qt.AlignCenter)
        self.chooseFilePath.setFont(QFont('Lucida Console',10))

        chooseFileButton = QPushButton()
        chooseFileButton.setFixedSize(40,40)
        chooseFileButton.setIcon(QIcon('Icons/folder.png'))
        chooseFileButton.clicked.connect(self.testFileClicked)

        chooseFileLayout = QHBoxLayout()
        chooseFileLayout.addWidget(choosefileText)
        chooseFileLayout.addWidget(self.chooseFilePath)
        chooseFileLayout.addWidget(chooseFileButton)
        chooseFileLayoutW = QWidget()
        chooseFileLayoutW.setLayout(chooseFileLayout)

        #File windows
        self.fileButton = QFileDialog()
        self.fileButton.setNameFilter("Text Files (*.txt)")
        self.fileButton.hide()

        #Single bit
        singleText = QLabel()
        singleText.setText("Single bit test")
        singleText.setAlignment(Qt.AlignLeft)
        singleText.setFont(QFont('Lucida Console',10))

        self.singleResult = QLabel()
        self.singleResult.setText("")
        self.singleResult.setAlignment(Qt.AlignRight)
        self.singleResult.setFont(QFont('Lucida Console',10))

        self.singleResult2 = QLabel()
        self.singleResult2.setText("")
        self.singleResult2.setAlignment(Qt.AlignCenter)
        self.singleResult2.setFont(QFont('Lucida Console',8))
        
        singleLayout = QHBoxLayout()
        singleLayout.addWidget(singleText)
        singleLayout.addWidget(self.singleResult2)
        singleLayout.addWidget(self.singleResult)
        singleLayoutW = QWidget()
        singleLayoutW.setLayout(singleLayout)

        #Runs
        runsText = QLabel()
        runsText.setText("Runs test")
        runsText.setAlignment(Qt.AlignLeft)
        runsText.setFont(QFont('Lucida Console',10))

        self.runsResult = QLabel()
        self.runsResult.setText("")
        self.runsResult.setAlignment(Qt.AlignRight)
        self.runsResult.setFont(QFont('Lucida Console',10))

        self.runsResult2 = QLabel()
        self.runsResult2.setText("")
        self.runsResult2.setAlignment(Qt.AlignCenter)
        self.runsResult2.setFont(QFont('Lucida Console',8))
        
        runsLayout = QHBoxLayout()
        runsLayout.addWidget(runsText)
        runsLayout.addWidget(self.runsResult2)
        runsLayout.addWidget(self.runsResult)
        runsLayoutW = QWidget()
        runsLayoutW.setLayout(runsLayout)

        #Long runs
        longRunsText = QLabel()
        longRunsText.setText("Long runs test")
        longRunsText.setAlignment(Qt.AlignLeft)
        longRunsText.setFont(QFont('Lucida Console',10))

        self.longRunsResult = QLabel()
        self.longRunsResult.setText("")
        self.longRunsResult.setAlignment(Qt.AlignRight)
        self.longRunsResult.setFont(QFont('Lucida Console',10))

        self.longRunsResult2 = QLabel()
        self.longRunsResult2.setText("")
        self.longRunsResult2.setAlignment(Qt.AlignCenter)
        self.longRunsResult2.setFont(QFont('Lucida Console',8))
        
        longRunsLayout = QHBoxLayout()
        longRunsLayout.addWidget(longRunsText)
        longRunsLayout.addWidget(self.longRunsResult2)
        longRunsLayout.addWidget(self.longRunsResult)
        longRunsLayoutW = QWidget()
        longRunsLayoutW.setLayout(longRunsLayout)

        #Poker
        pokerText = QLabel()
        pokerText.setText("Poker test")
        pokerText.setAlignment(Qt.AlignLeft)
        pokerText.setFont(QFont('Lucida Console',10))

        self.pokerResult = QLabel()
        self.pokerResult.setText("")
        self.pokerResult.setAlignment(Qt.AlignRight)
        self.pokerResult.setFont(QFont('Lucida Console',10))

        self.pokerResult2 = QLabel()
        self.pokerResult2.setText("")
        self.pokerResult2.setAlignment(Qt.AlignCenter)
        self.pokerResult2.setFont(QFont('Lucida Console',8))
        
        pokerLayout = QHBoxLayout()
        pokerLayout.addWidget(pokerText)
        pokerLayout.addWidget(self.pokerResult2)
        pokerLayout.addWidget(self.pokerResult)
        pokerLayoutW = QWidget()
        pokerLayoutW.setLayout(pokerLayout)


        self.singleButton = QRadioButton("Single bit test")
        self.singleButton.setChecked(True)

        self.runsButton = QRadioButton("Runs test")
        self.longrunsButton = QRadioButton("Long runs test")
        self.pokerButton = QRadioButton("Poker test")

        testTypeButtonsLayout = QHBoxLayout()
        testTypeButtonsLayout.addWidget(self.singleButton)
        testTypeButtonsLayout.addWidget(self.runsButton)
        testTypeButtonsLayout.addWidget(self.longrunsButton)
        testTypeButtonsLayout.addWidget(self.pokerButton)
        testTypeButtonsLayout.setAlignment(Qt.AlignHCenter)
        testTypeButtonsLayoutW = QWidget()
        testTypeButtonsLayoutW.setLayout(testTypeButtonsLayout)

        #Test button
        self.testButton = QPushButton()
        self.testButton.setText("TEST")
        self.testButton.setFont(QFont('Lucida Console',10))
        self.testButton.clicked.connect(self.testClicked)

        #Layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(titleLayoutW)
        self.layout.addWidget(self.statusText)
        self.layout.addWidget(chooseFileLayoutW)
        self.layout.addWidget(singleLayoutW)
        self.layout.addWidget(runsLayoutW)
        self.layout.addWidget(longRunsLayoutW)
        self.layout.addWidget(pokerLayoutW)
        #self.layout.addWidget(testTypeButtonsLayoutW)
        self.layout.addWidget(self.testButton)
        self.setLayout(self.layout)

    def testFileClicked(self):
        """Sets file path"""
        self.fileButton.show()

        if self.fileButton.exec():
            files = self.fileButton.selectedFiles()
            self.chooseFilePath.setText(files[0])            

    def singleTest(self, data):
        num = data.count('1')
        return num > 9725 and num < 10275, "Number of 1: "+str(num)

    def runsTest(self, data):
        ranges = {
            1 : [2315, 2685],
            2 : [1114, 1386],
            3 : [527, 723],
            4 : [240, 384],
            5 : [103, 209],
            6 : [103, 209]
        }
        zeros = re.findall(r"0+", data)
        ones = re.findall(r"1+", data)
        zerosMap = {}
        onesMap = {}
        for i in range (1, 7):
            zerosMap[i] = 0
            onesMap[i] = 0
        for runs in zeros:
            if len(runs) > 6:
                zerosMap[6] += 1
            else:
                zerosMap[len(runs)] += 1
        for runs in ones:
            if len(runs) > 6:
                onesMap[6] += 1
            else:
                onesMap[len(runs)] += 1

        result = 0
        for i in range(1,7):
            if zerosMap[i] > ranges.get(i)[0] and zerosMap[i] < ranges.get(i)[1]:
                result += 1
            if onesMap[i] > ranges.get(i)[0] and onesMap[i] < ranges.get(i)[1]:
                result += 1
        return result == 12, zerosMap, onesMap

    def longRunsTest(self, data):
        if re.search(r"(0{26})|(1{26})", data) is None:
            return True, "It doesn't exist 26-character long run"
        else:
            return False, "It exists 26-character long run"

    def pokerTest(self, data):
        combinations = {
            '0000': 0,
            '0001': 0,
            '0010': 0,
            '0011': 0,
            '0100': 0,
            '0101': 0,
            '0110': 0,
            '0111': 0,
            '1000': 0,
            '1001': 0,   
            '1010': 0,
            '1011': 0,
            '1100': 0,
            '1101': 0,
            '1110': 0,
            '1111': 0
        }
        for i in range (0,len(data),4):
            tmp = ""
            for j in range (4):
                tmp += data[i + j]
            combinations[tmp] += 1

        sum = 0
        for v in combinations.values():
            sum += (v ** 2)
        x = ((16 / 5000) * sum) - 5000
        return x > 2.16 and x < 46.17, "X = "+str(x)

    def testClicked(self):
        """Tests file"""
        f = open(self.chooseFilePath.text(), 'r')
        with f:
            data = f.read()
            f.close()

        if len(data) != 20000:
            self.statusText.setStyleSheet('color: red')
            self.statusText.setText("File must contain 20 000 characters!")
            QtTest.QTest.qWait(3000)
            self.statusText.setStyleSheet('color: black')
            self.statusText.setText("Choose file and test type")

        result(self.singleResult, self.singleTest(data)[0])
        result(self.runsResult, self.runsTest(data)[0])
        result(self.longRunsResult, self.longRunsTest(data)[0])
        result(self.pokerResult, self.pokerTest(data)[0])

        resultMsg(self.singleResult2, self.singleTest(data)[1])
        resultMsg(self.runsResult2, self.runsTest(data)[1], self.runsTest(data)[2])
        resultMsg(self.longRunsResult2, self.longRunsTest(data)[1])
        resultMsg(self.pokerResult2, self.pokerTest(data)[1])

    def infoWindow(self):
        """Opens info window"""
        infoW = QMessageBox()
        infoW.setWindowTitle("Tests")
        infoW.setWindowIcon(QIcon('Icons/info.png'))
        #infoW.setFont(QFont('Lucida Console'))
        #infoW.setStyleSheet("QLabel{min-width: 900px;}")
        f = open("info4.txt", "r", encoding='utf8')
        text = f.read()
        infoW.setText(text)
        infoW.setWindowModality(Qt.ApplicationModal)
        infoW.exec_()

def result(label, result):
    if result:
        label.setStyleSheet('color: green')
        label.setText("Test passed!")
    else:
        label.setStyleSheet('color: red')
        label.setText("Test failed!")

def resultMsg(label, msg1, msg2 = None):
    if msg2 is None:
        label.setText(str(msg1))
    else:
        label.setText("0: "+str(msg1)+'\n1: '+str(msg2))