from math import radians
import numpy as np
import bitstring
from bitstring import BitArray
from EncryptingFiles import Encryptor


class FileEncryptor:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def Encrypt(self, path):
        f = BitArray(open(path, "rb").read())
        print(f.bin)
        out = BitArray()
        for i in range(0, f.__len__(), self.algorithm.DataSize):
            out += self.algorithm.Encrypt(f[i:i+self.algorithm.DataSize])
        print(out.bin)
        return out


def main():
    s = FileEncryptor(Encryptor.TripleDES("4leyyfajnykey")).Encrypt("test.txt")

    f = open("test.txt", "rb")
    Bytes = f.read()
    Bits= BitArray(Bytes)
    print(Bits.__len__())
    print(Bits[0:64].bin)
    key = "4leyy"
    out = Encryptor.TripleDES(key).Encrypt(Bits[0:64])
    print(out.bin)
    out = Encryptor.TripleDES(key).Decrypt(out)
    print(out.bin)
    f.close()

main()