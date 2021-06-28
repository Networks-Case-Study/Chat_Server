import socket
import random


class PhysicalLayer():
    def __init__(self, bits):
        self.message = ""
        self.bits = bits
        self.decodedMessage = ""
        self.time = list(range(len(self.bits)))
        self.manchesterEncoding = bits
        self.manchesterYVal = []
        self.originalYVal = []

    def decode(self, generator):
        temp = ""
        print("\nManchester Encoding                 : \n" + str(self.bits))
        yVal = [int(x) for x in list(self.bits)]
        temp = []
        for val in yVal:
            if val == 0:
                temp.append(-1)
            else:
                temp.append(1)
        yVal = temp
        self.manchesterYVal = yVal
        temp = ""
        for i in range(0, len(self.bits), 2):
            s = self.bits[i: i + 2]
            if s == "01":
                temp += "1"
            elif s == "10":
                temp += "0"
        self.bits = temp
        tempOriginalYVal = [int(x) for x in self.bits]
        for y in tempOriginalYVal:
            self.originalYVal.append(y)
            self.originalYVal.append(y)
        print("\nOriginal Encoding With CRC Remainder     : \n" + str(self.bits))
        choice = input(
            "\nPress 1 for delibertely inserting error bits yes else give any other input : ")
        if choice == "1":
            temp = list(self.bits)

            for i in range(5):
                index = random.randint(0, len(self.bits) - 1)
                if temp[index] == "0":
                    temp[index] = "1"
                elif temp[index] == "1":
                    temp[index] = "0"
            self.bits = "".join(temp)
            print("\nOriginal Encoding With CRC Remainder After Introducing Deliberate Errors     : \n" + str(self.bits))
        CRCchecksum = DataLinkLayer(self.bits, generator).CRCdetectError()
        print("\nCRC Remainder\t\t: \n" + str(CRCchecksum))
        if CRCchecksum == '0' * (len(generator) - 1):
            self.bits = self.bits[:-(len(generator) - 1)]
            if len(self.bits) % 8 != 0:
                print("\nError detected in data. Number of bits not a multiple of 8.\n")
                return None
            else:
                print("\nNo Error in bits transmitted from current frame.")
                print("\nOriginal Encoding Without CRC Remainder : \n" + str(self.bits))
                return self.bitsToString()

        else:
            print("\nError detected in data. CRC Remainder is not equal to " +
                  str('0' * (len(generator) - 1)))
            return None

    def bitsToString(self):

        chars = []
        bitsArray = []
        for i in self.bits:
            bitsArray.append(int(i))
        for b in range(len(bitsArray) // 8):
            byte = bitsArray[b*8:(b+1)*8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        self.decodedMessage = ''.join(chars)
        return self.decodedMessage


class DataLinkLayer():
    def __init__(self, bits, generator):
        self.bits = bits
        self.keyLength = len(generator)
        self.appendedData = self.bits + "0" * (self.keyLength - 1)
        self.generator = generator

    def CRCdetectError(self):
        divisor = self.generator
        divident = self.appendedData
        numBits = len(self.generator)
        subpartSubstring = self.appendedData[0: numBits]

        while numBits < len(self.appendedData):
            if subpartSubstring[0] == '1':
                subpartSubstring = self.XOR(
                    self.generator, subpartSubstring) + self.appendedData[numBits]

            else:
                subpartSubstring = self.XOR(
                    '0'*numBits, subpartSubstring) + divident[numBits]
            numBits += 1
        if subpartSubstring[0] == '1':
            subpartSubstring = self.XOR(divisor, subpartSubstring)
        else:
            subpartSubstring = self.XOR('0' * numBits, subpartSubstring)
        checksum = subpartSubstring
        return checksum

    def XOR(self, messagePartition, generator):
        self.xor = ""
        for bit1, bit2 in zip(messagePartition, generator):
            if bit1 == bit2:
                self.xor = self.xor + "0"
            else:
                self.xor = self.xor + "1"
        return self.xor[1:]


if __name__ == "__main__":
    print("Welcome Client ")

    generator = input("Enter the generator function in 0s and 1s : ")
    finalDecodedMessage = ""
    while True:
        s = socket.socket()
        port = 10000
        try:
            s.connect(("127.0.0.1", port))
        except:
            break
        receivedMessage = s.recv(1024).decode()

        print("Received message is ", receivedMessage)

        physicalLayer = PhysicalLayer(receivedMessage)
        decodedMessage = physicalLayer.decode(generator)

        if decodedMessage != None:
            print("\nDecoded Frame Message     : " + str(decodedMessage))
            finalDecodedMessage += str(decodedMessage)
        else:
            print("\nError detected in data by CRC (Cyclic Redundancy Check).")
        print("--------------------------------------")

    print("\nFinal Decoded Message : " + str(finalDecodedMessage))
    print("--------------------------------------")
    s.close()
