from math import radians
import numpy as np
from bitstring import BitArray
from EncryptingFiles import Encryptor

def main():
    f = open("test.txt", "rb")

    Bytes = f.read()
    Bits= BitArray(Bytes)
    example = BitArray(length=64)
    example[4] = 1
    print(example.bin)
    out = Encryptor.DES.Encrypt(example, Bits[0:48])
    print(out.bin)
    out = Encryptor.DES.Decrypt(out, Bits[0:48])
    print(out.bin)
    f.close()

main()