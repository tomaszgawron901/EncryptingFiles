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
    print(Bits[0:32])
    print(Encryptor.SBlock.Encrypt(Bits[0:32], Bits[32:80]))
    for b in Bits[0:64]:
        print(b)
    print(Bits[0:64])
    print(Bytes.__len__())
    f.close()

main()