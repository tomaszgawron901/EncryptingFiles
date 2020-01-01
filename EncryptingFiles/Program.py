from math import radians
import numpy as np
import bitstring
from bitstring import BitArray
from EncryptingFiles import Encryptor


def main():
    f = open("test.txt", "rb")

    Bytes = f.read()
    Bits= BitArray(Bytes)
    print(Bits.__len__())
    print(Bits[0:64].bin)
    keys = Encryptor.TripleDES.CreateKey("4le fajny klucz")
    out = Encryptor.TripleDES.Encrypt(Bits[0:64], keys)
    print(out.bin)
    out = Encryptor.TripleDES.Decrypt(out, keys)
    print(out.bin)
    f.close()

main()