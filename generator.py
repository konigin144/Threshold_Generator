import numpy
from random import random,randint

class ThresholdFunction():
    LFSRregs = []       # array containing current states of registers

    xorTable = {
        20 : [17,20],
        21 : [19,21],
        22 : [21,22],
        23 : [18,23],
        24 : [20,21,23,24],
        25 : [22,25],
        26 : [20,24,25,26],
        27 : [22,25,26,27],
        28 : [25,28],
        29 : [27,29],
        30 : [24,26,29,30],
        31 : [28,31],
        32 : [25,27,29,30,31,32],
        33 : [20,33],
        34 : [27,28,29,32,33,34],
        35 : [33,35],
        36 : [25,36],
        37 : [31,33,36,37],
        38 : [32,33,37,38],
        39 : [35,39],
        40 : [35,36,37,40],
        41 : [38,41],
        42 : [35,38,39,40,41,42],
        43 : [37,39,40,43],
        44 : [38,39,42,44],
        45 : [41,42,44,45],
        46 : [38,39,40,46],
        47 : [42,47],
        48 : [39,41,44,48],
        49 : [40,49],
        50 : [46,47,48,50],
        51 : [45,48,50,51],
        52 : [49,52],
        53 : [47,51,52,53],
        54 : [46,48,51,54],
        55 : [31,55],
        56 : [49,52,54,56],
        57 : [50,57],
        58 : [39,58],
        59 : [52,55,57,59],
        60 : [59,60]
    }
    
    def initial(self, sizesArr): #Stany poczatkowe same 0 i 1 na końcu - 2
        # Sets LFSR registers' initial states as 0s and one 1 in the end.
        initRegsArr = []
        for i in sizesArr:
            temp = [0] * i
            temp[i-1] = 1
            initRegsArr.append(temp[:])
            print(temp)
        return initRegsArr
        
    def randomInitial(self, sizesArr):
        # Sets LFSR registers' initial states as random values. The last element is always 1.
        initRegsArr = []
        for i in sizesArr:
            temp = []
            for j in range(i-1):
                temp.append(randint(0,1))
            temp.append(1)
            initRegsArr.append(temp[:])
        return initRegsArr

    def definedInitial(self, valuesArr):
        initRegsArr = []
        for values in valuesArr:
            initRegsArr.append(values)
        return initRegsArr

    def xor(self, reg): #POMOCNICZA
        # XOR operation on bits of given register

        # gets values to XOR
        arrLen = len(reg)
        indexesToXor = self.xorTable.get(arrLen)       # bits' indexes
        valuesToXor = []                               # bits' values
        for i in indexesToXor:
            valuesToXor.append(reg[i-1])
        result = valuesToXor[0]

        # XOR operation
        for i in range(1, len(valuesToXor)): 
            for j in range(i, len(valuesToXor)): 
                for k in range(i, j + 1): 
                    result = result ^ valuesToXor[k] 
        return result

    def LFSR(self, reg): #Funkcja przetwarza jedno taktowanie jednego rejestru - POMOCNICZA
        # Processes one tact of one LFSR register
        output = reg[len(reg)-1]
        xorResult = self.xor(reg)
        del reg[len(reg)-1]
        reg.insert(0,xorResult)
        #self.LFSRregs.append(reg[:])
        return output

    def checkRelativelyFirst(self, a, b): #sprawdzenie czy funkcja jest relatywnie pierwsza - POMOCNICZA
        # Checks if given two numbers are relatively first. Returns True if yes, returns False otherwise.
        if b > 0:
            return self.checkRelativelyFirst(b, a%b)
        return a

    def randomSizeArray(self, numOfRegs): #losowanie rozmiarów tablic -- 1
        # Generate random sizes for a given number of arrays.
        sizesArr = []
        for i in range(numOfRegs):
            if i == 0:
                while True:
                    size = randint(20,60)
                    if size % 2 == 1:
                        sizesArr.append(size)
                        break
            else:
                while True:
                        temp = 1
                        size = randint(20,60)
                        for j in sizesArr:
                            if self.checkRelativelyFirst(j, size) == 1 and size not in sizesArr and size % 2 == 1:
                                temp += 1
                        if temp == len(sizesArr)+1:
                            sizesArr.append(size)
                            break
                        """else:
                            arrSize = randint(20,60)
                            temp = 1"""
        return sizesArr

    def generate(self): #funkcja tworzy input z rejestrów dla funkcji progowej - 3
        # Prepares an input for threshold function. Connects outputs from arrays.
        resultArr = []
        for arr in self.LFSRregs:
            resultArr.append(self.LFSR(arr))    
        return resultArr


    def thresholdFunction(self, n): #Funkcja progowa
        # Generates 0 or 1 basing on outputs of LFSR registers.
        sum = 0
        resultArr = []
        for i in range(n):
            temp = self.generate()
            for j in temp:
                sum += j
            if float(sum) > float(len(self.LFSRregs)/2):
                resultArr.append(1)
            else:
                resultArr.append(0)
            sum = 0
        #print(resultArr)
        return resultArr

    def __init__(self, numRegs, initType, regVals=None):
        # 0 - 000...0001
        # 1 - full random
        sizesArr = self.randomSizeArray(numRegs)    # array of arrays' sizes
        if regVals is not None:
            self.LFSRregs = self.definedInitial(regVals)
        else:
            if initType == 0:
                self.LFSRregs = self.initial(sizesArr)
            else:
                self.LFSRregs = self.randomInitial(sizesArr)
        

        #print(sizesArr)
        #print(self.LFSRregs)



"""
arr1 = randomSizeArray(5)
arr2 = initial(arr1)
arr3 = randomInitial(arr2)
arr4 = thresholdFunction(arr3,5,1000000)
f = open("file.txt", "w")
for i in arr4:
    f.write(str(i))
f.close()"""
