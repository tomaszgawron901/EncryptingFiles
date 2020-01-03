from math import radians
import numpy as np
import bitstring
from bitstring import BitArray
from bitarray import bitarray
from EncryptingFiles import Encryptor


class FileEncryptor:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def ReadFile(self, path):
        with open(path, "rb") as file:
            out = bitarray()
            out.fromfile(file)
        return out

    def WriteFile(self, bits, path):
        file = open(path, "wb")
        bits.tofile(file)
        file.close()

    def Encrypt(self, path):
        out = self.algorithm.Encrypt(self.ReadFile(path))
        self.WriteFile(out.reshape((1, -1)), path)

    def Decrypt(self, path):
        f = BitArray(self.ReadFile(path))
        out = BitArray()
        for i in range(0, f.__len__(), self.algorithm.DataSize):
            out += self.algorithm.Decrypt(f[i:i+self.algorithm.DataSize])
        self.WriteFile(out, path)


def main():
    f = FileEncryptor(None).ReadFile("test.txt")
    FileEncryptor(Encryptor.DES("4leyyf")).Encrypt("test.txt")
    FileEncryptor(Encryptor.DES("4leyyf")).Decrypt("test.txt")


main()
