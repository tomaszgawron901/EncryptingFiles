from math import radians
import numpy as np
import bitstring
from bitstring import BitArray
from EncryptingFiles import Encryptor


class FileEncryptor:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def ReadFile(self, path):
        file = open(path, "rb")
        out = file.read()
        file.close()
        return out

    def WriteFile(self, bits, path):
        file = open(path, "wb")
        bits.tofile(file)
        file.close()

    def Encrypt(self, path):
        f = BitArray(self.ReadFile(path))
        out = BitArray()
        for i in range(0, f.__len__(), self.algorithm.DataSize):
            out += self.algorithm.Encrypt(f[i:i+self.algorithm.DataSize])
        self.WriteFile(out, path)

    def Decrypt(self, path):
        f = BitArray(self.ReadFile(path))
        out = BitArray()
        for i in range(0, f.__len__(), self.algorithm.DataSize):
            out += self.algorithm.Decrypt(f[i:i+self.algorithm.DataSize])
        self.WriteFile(out, path)


def main():
    FileEncryptor(Encryptor.TripleDES("4leyyfajnykey")).Encrypt("test.txt")
    FileEncryptor(Encryptor.TripleDES("4leyyfajnykey")).Decrypt("test.txt")


main()
