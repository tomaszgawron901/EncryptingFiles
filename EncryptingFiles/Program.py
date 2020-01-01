from math import radians
import numpy as np
from bitstring import BitArray
from EncryptingFiles import Encryptor

def main():
    f = open("test.txt", "rb")

    Bytes = f.read()
    Bits= BitArray(Bytes)
    print(Bits[0:64].bin)
    keys = [Bits[0:64], Bits[10:74], Bits[20:84]]
    out = Encryptor.TripleDES.Encrypt(Bits[0:64], keys)
    print(out.bin)
    out = Encryptor.TripleDES.Decrypt(out, keys)
    print(out.bin)
    f.close()

main()