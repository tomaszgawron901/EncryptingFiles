import numpy as np
from bitarray import bitarray
import Encryptor

import enum
import os

class Operations(enum.Enum):
    Encrypt = 0
    Decrypt = 1


class Algorithms:
    DES = Encryptor.DES
    TDES = Encryptor.TripleDES


class FileEncryptor:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    # Read bits from a file as bitarray.
    @staticmethod
    def ReadFile(path):
        with open(path, "rb") as file:
            out = bitarray()
            out.fromfile(file)
        return out

    # Write bitarray to a file.
    @staticmethod
    def WriteFile(bits, path):
        file = open(path, "wb")
        bits.tofile(file)
        file.close()

    # Returns encrypted bitarray.
    def Encrypt(self, file):
        out = self.algorithm.DataOptimalize(file)
        out = self.algorithm.Encrypt(out)
        out = out.reshape((1, -1))
        out = np.squeeze(out)
        out = out.tolist()
        out = bitarray(out)
        return out

    # Returns decrypted bitarray.
    def Decrypt(self, file):
        out = self.algorithm.DataOptimalize(file)
        out = self.algorithm.Decrypt(out)
        out = out.reshape((1, -1))
        out = np.squeeze(out)
        out = out.tolist()
        out = bitarray(out)
        return out


class Help:
    helpCharacter = '?'

    @staticmethod
    def path():
        print("Path name example: C:\\Users\\Bob\\Desktop\\example.txt")

    @staticmethod
    def operation():
        print("Enter 'ENC' to chose file encryption.")
        print("Enter 'DEC' to chose file decryption.")

    @staticmethod
    def algorithm():
        print("Enter 'DES' to chose DES algorithm.")
        print("Enter 'TDES' to chose triple DES algorithm.")

    @staticmethod
    def DESkey():
        print("Key is a string of 7 characters.")

    @staticmethod
    def TDESkey():
        print("Key is a string of 21 characters.")


class Info:
    @staticmethod
    def baseInfo():
        return "type '%s' to show help or 'B' to go back." % Help.helpCharacter

    @staticmethod
    def path():
        print("Enter full file name or type '%s' to show help." % Help.helpCharacter)

    @staticmethod
    def operation():
        print("Enter operation type (ENC - encryption, DEC - decryption) ," + Info.baseInfo())

    @staticmethod
    def algorithm():
        print("Enter algorithm name (DES or TDES) ," + Info.baseInfo())

    @staticmethod
    def key():
        print("Enter key ," + Info.baseInfo())


class Controller:
    @staticmethod
    def clear():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def writeHelp(helpFunction):
        helpFunction()
        print("Pres Enter to continue.")
        input()

    def __init__(self):
        self.pathString = None
        self.file = None
        self.operation = None
        self.algorithm = None
        self.key = None

    def start(self):
        if self.__initialize():
            self.__execute()
        else:
            raise "Something went wrong"

    def __execute(self):
        if self.operation == Operations.Encrypt:
            FileEncryptor.WriteFile(FileEncryptor(self.algorithm(self.key)).Encrypt(self.file), self.pathString)
        elif self.operation == Operations.Decrypt:
            FileEncryptor.WriteFile(FileEncryptor(self.algorithm(self.key)).Decrypt(self.file), self.pathString)

    def __initialize(self):
        return self.__pathPhase()

    def __pathPhase(self):
        Controller.clear()
        while True:
            Info.path()
            consoleInput = input()
            if consoleInput.__len__() == 1 and consoleInput[0] == '?':
                Controller.clear()
                Controller.writeHelp(Help.path)
                Controller.clear()
                continue
            else:
                try:
                    self.pathString = consoleInput
                    self.file = FileEncryptor.ReadFile(self.pathString)
                    if self.__operationPhase():
                        return True
                    else:
                        Controller.clear()
                        continue
                except FileNotFoundError:
                    Controller.clear()
                    print("File with given path does not exist. Try again.")
                    continue

    def __operationPhase(self):
        Controller.clear()
        while True:
            Info.operation()
            consoleInput = input()
            if consoleInput.__len__() == 1 and consoleInput[0] == '?':
                Controller.clear()
                Controller.writeHelp(Help.operation)
                Controller.clear()
                continue
            elif consoleInput.__len__() == 1 and consoleInput[0].upper() == 'B':
                return False
            else:
                if consoleInput.upper() == "ENC" or consoleInput.upper() == "DEC":
                    if consoleInput.upper() == "ENC":
                        self.operation = Operations.Encrypt
                    else:
                        self.operation = Operations.Decrypt
                    if self.__algorithmPhase():
                        return True
                    else:
                        Controller.clear()
                        continue
                else:
                    Controller.clear()
                    print("Invalid operation name.")
                    continue

    def __algorithmPhase(self):
        Controller.clear()
        while True:
            Info.algorithm()
            consoleInput = input()
            if consoleInput.__len__() == 1 and consoleInput[0] == '?':
                Controller.clear()
                Controller.writeHelp(Help.algorithm)
                Controller.clear()
                continue
            elif consoleInput.__len__() == 1 and consoleInput[0].upper() == 'B':
                return False
            else:
                if consoleInput.upper() == "DES":
                    self.algorithm = Algorithms.DES
                    if self.__DESKeyPhase():
                        return True
                    else:
                        continue
                elif consoleInput.upper() == "TDES":
                    self.algorithm = Algorithms.TDES
                    if self.__TDESKeyPhase():
                        return True
                    else:
                        continue
                else:
                    Controller.clear()
                    print("Invalid algorithm name.")
                    continue

    def __DESKeyPhase(self):
        Controller.clear()
        while True:
            Info.key()
            consoleInput = input()
            if consoleInput.__len__() == 1 and consoleInput[0] == '?':
                Controller.clear()
                Controller.writeHelp(Help.DESkey)
                Controller.clear()
                continue
            elif consoleInput.__len__() == 1 and consoleInput[0].upper() == 'B':
                return False
            else:
                if consoleInput.__len__() == 7:
                    self.key = consoleInput
                    return True
                else:
                    Controller.clear()
                    print("Invalid key length. DES key must have 7 characters.")
                    continue

    def __TDESKeyPhase(self):
        Controller.clear()
        while True:
            Info.key()
            consoleInput = input()
            if consoleInput.__len__() == 1 and consoleInput[0] == '?':
                Controller.clear()
                Controller.writeHelp(Help.TDESkey)
                Controller.clear()
                continue
            elif consoleInput.__len__() == 1 and consoleInput[0].upper() == 'B':
                return False
            else:
                if consoleInput.__len__() == 21:
                    self.key = consoleInput
                    return True
                else:
                    Controller.clear()
                    print("Invalid key length. Triple DES key must have 21 characters.")
                    continue


def main():
    while True:
        Controller().start()
        print("Enter 'C' to continue application.")
        print("Enter other key to close application.")
        if input().upper() != "C":
            break


if __name__ == "__main__":
    main()

