import socket


class PhysicalLayer():
    def __init__(self, message):

        self.message = message
        self.bits = ""
        self.encodedMessage = ""

    def encode(self, generator):
        self.stringToBits()
        print("\nOriginal Message Bits: \n" + str(self.bits))

        checksum = DataLinkLayer(self.bits, generator).encodeWithCRC()

        print("\nCRC Value: \n" + str(checksum))

        self.bits = self.bits + checksum
        for bit in self.bits:
            if bit == "0":
                self.encodedMessage += "10"
            elif bit == "1":
                self.encodedMessage += "01"
        print("\nOriginal Message Bits With CRC Value  : \n" + str(self.bits))
        print("\nManchester Encoding                   : \n" +
              str(self.encodedMessage))
        return self.encodedMessage

    def stringToBits(self):
        temp = []
        for c in self.message:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            temp.extend([int(b) for b in bits])
        self.bits = ""
        for b in temp:
            self.bits += str(b)


class DataLinkLayer():

    def __init__(self, bits, generator):
        self.bits = bits
        self.keyLength = len(generator)
        self.appendedData = self.bits + "0" * (self.keyLength - 1)
        self.generator = generator

    def XOR(self, generator, messagePartition):
        self.xor = ""
        for bit1, bit2 in zip(messagePartition, generator):
            if bit1 == bit2:
                self.xor = self.xor + "0"
            else:
                self.xor = self.xor + "1"
        return self.xor[1:]

    def encodeWithCRC(self):
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


if __name__ == "__main__":
    s = socket.socket()
    port = 10000
    s.bind(("127.0.0.1", port))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created and binded to port number " + str(port))
    s.listen(5)
    print("Socket listening.")
    print("Ensure the Generator function is same in both Client and Server side, Otherwise message would be corrupted")
    fullMessage = input("\nEnter the message you want to send : ")
    generator = input(
        "\n\nEnter the generator function in (0s, 1s) Eg:- 0010 : ")
    print("\nWaiting for client...")
    framesize = int(input("Enter frame size"))
    framesToSend = [fullMessage[i:i+framesize]
                    for i in range(0, len(fullMessage), framesize)]
    for i in range(len(framesToSend)):
        messageToSend = framesToSend[i]
        print("\nSending Frame Number " + str(i))
        c, addr = s.accept()
        print("\nClient connection received " + str(addr))
        encodedMessage = PhysicalLayer(messageToSend).encode(generator)
        print("\nEncoded input to    : " + str(encodedMessage))
        c.send(encodedMessage.encode())
        print("--------------------------------------")
        c.close()
