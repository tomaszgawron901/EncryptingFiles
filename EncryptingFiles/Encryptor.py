import numpy as np
from bitstring import BitArray


class DES:
    @staticmethod
    def Encrypt(bytes64, key):
        pass


class DESCell:
    @staticmethod
    def Encrypt(l_bits, r_bits, key):
        if (type(l_bits) is not BitArray) or (l_bits.__len__() != 32):
            raise ("l_bits wrong defined.")
        if (type(r_bits) is not BitArray) or (r_bits.__len__() != 32):
            raise ("r_bits wrong defined.")
        if (type(key) is not BitArray) or (key.__len__() != 32):
            raise ("key wrong defined.")

        return r_bits, l_bits


class SBlock:
    @staticmethod
    def Encrypt(bits32, key):
        if (type(bits32) is not BitArray) or (bits32.__len__() != 32):
            raise ("bits32 wrong defined.")
        if (type(key) is not BitArray) or (key.__len__() != 48):
            raise ("key wrong defined.")
        out = ExpendingPermutation.Expend(bits32)
        out = out.__xor__(key)
        out = SRow.Reduce(out)
        return out


class SRow:
    __LookUpTable = [
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]

    ]

    @classmethod
    def Reduce(cls, bites48):
        if (type(bites48) is not BitArray) or (bites48.__len__() != 48):
            raise ("bites48 wrong defined.")
        out = BitArray()
        for i in range(0, 8, 1):
            out += SCell.Execute(bites48[i:i+6], cls.__LookUpTable[i])
        return out


class SCell:
    @staticmethod
    def Execute(bits6, table):
        if (type(bits6) is not BitArray) or (bits6.__len__() != 6):
            raise ("bits6 wrong defined.")
        x = (bits6[0:1] + bits6[5:6]).uint
        y = bits6[1:5].uint
        out = BitArray(length=4)
        out.uint = table[x][y]
        return out


class ExpendingPermutation:
    __LookUpTable = [
        31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10,
        11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20,
        21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0
    ]

    @classmethod
    def Expend(cls, bits):
        if (type(bits) is not BitArray) or (bits.__len__() != 32):
            raise ("bits wrong defined.")
        output = BitArray(length=48)
        for i in range(0, 48, 1):
            output[i] = bits[cls.__LookUpTable[i]]
        return output
