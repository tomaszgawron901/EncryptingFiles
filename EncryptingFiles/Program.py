from math import radians
import numpy as np
import bitstring
from bitstring import BitArray
from EncryptingFiles import Encryptor


class FileEncryptor:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def Encrypt(self, path):
        pass


def main():
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