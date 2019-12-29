from math import radians
import numpy as np
from bitstring import BitArray
from EncryptingFiles import Encryptor

def main():
    #encryptor = Encryptor()
    f = open("test.txt", "rb")
    #encryptor.Encrypt(f.read())

    Bytes = f.read()
    Bits= BitArray(Bytes)
    example = BitArray(length=64)
    example[0] = 1
    print(example.bin)
    print(Encryptor.DES.Encrypt(example, Bits[0:48]).bin)
    f.close()

main()