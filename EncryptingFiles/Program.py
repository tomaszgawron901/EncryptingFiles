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
        out = self.algorithm.DataOptimalize(self.ReadFile(path))
        out = self.algorithm.Encrypt(out)
        out = out.reshape((1, -1))
        out = np.squeeze(out)
        out = out.tolist()
        out = bitarray(out)
        self.WriteFile(out, path)

    def Decrypt(self, path):
        out = self.algorithm.DataOptimalize(self.ReadFile(path))
        out = self.algorithm.Decrypt(out)
        out = out.reshape((1, -1))
        out = np.squeeze(out)
        out = out.tolist()
        out = bitarray(out)
        self.WriteFile(out, path)


def main():
    FileEncryptor(Encryptor.TripleDES("4leyyf")).Encrypt("picture.jpg")
    FileEncryptor(Encryptor.TripleDES("4leyyf")).Decrypt("picture.jpg")


main()
