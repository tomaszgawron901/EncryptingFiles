import numpy as np
from bitstring import BitArray
import abc


class DESKeyManager(abc.ABC):
    _BitRotationTable = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    class PermutedChoice1:
        __LeftLookUpTable = [
            56, 48, 40, 32, 24, 16, 8,
            0, 57, 49, 41, 33, 25, 17,
            9, 1, 58, 50, 42, 34, 26,
            18, 10, 2, 59, 51, 43, 35
        ]

        __RightLookUpTable = [
            62, 54, 46, 38, 30, 22, 14,
            6, 61, 53, 45, 37, 29, 21,
            13, 5, 60, 52, 44, 36, 28,
            20, 12, 4, 27, 19, 11, 3
        ]

        @classmethod
        def Execute(cls, key64):
            if (type(key64) is not BitArray) or (key64.__len__() != 64):
                raise ("key64 wrong defined.")
            leftOut = BitArray(length=28)
            rightOut = BitArray(length=28)
            for i in range(0, 28):
                leftOut[i] = key64[cls.__LeftLookUpTable[i]]
                rightOut[i] = key64[cls.__RightLookUpTable[i]]
            return leftOut, rightOut

    class PermutedChoice2:
        __LookUpTable = [
            13, 16, 10, 23, 0, 4,
            2, 27, 14, 5, 20, 9,
            22, 18, 11, 3, 25, 7,
            15, 6, 26, 19, 12, 1,
            40, 51, 30, 36, 46, 54,
            29, 39, 50, 44, 32, 47,
            43, 48, 38, 55, 33, 52,
            45, 41, 49, 35, 28, 31
        ]

        @classmethod
        def Execute(cls, key56):
            if (type(key56) is not BitArray) or (key56.__len__() != 56):
                raise ("key56 wrong defined.")
            out = BitArray(length=48)
            for i in range(0, 48):
                out[i] = key56[cls.__LookUpTable[i]]
            return out

    def __init__(self, key):
        if (type(key) is not BitArray) or (key.__len__() != 64):
            raise ("key wrong defined.")
        self.leftKey, self.rightKey = self.PermutedChoice1.Execute(key)
        self.rotationNumber: int = 0

    @abc.abstractmethod
    def GetKey(self):
        raise ("Not implemented Exception.")

    @abc.abstractmethod
    def Rotate(self):
        raise ("Not implemented Exception.")

    @staticmethod
    def RotateBits(bits, rotation):
        if type(bits) is not BitArray:
            raise ("bits wrong defined.")
        rotation = rotation % bits.__len__()
        return bits[rotation:]+bits[:rotation]

    def _GetCurrentRotation(self):
        return self._BitRotationTable[self.rotationNumber]


class DESEncryptionKeyManager(DESKeyManager):
    def __init__(self, key):
        super().__init__(key)
        self.rotationNumber = 0

    def GetKey(self):
        self.Rotate()
        return self.PermutedChoice2.Execute(self.leftKey+self.rightKey)

    def Rotate(self):
        if self.rotationNumber >= self._BitRotationTable.__len__() or self.rotationNumber < 0:
            raise ("Argument out of range Exception.")
        self.leftKey = self.RotateBits(self.leftKey, self._GetCurrentRotation())
        self.rightKey = self.RotateBits(self.rightKey, self._GetCurrentRotation())

        self.rotationNumber += 1
        if self.rotationNumber >= self._BitRotationTable.__len__():
            self.rotationNumber = 0


class DESDescriptionKeyManager(DESKeyManager):
    def __init__(self, key):
        super().__init__(key)
        self.rotationNumber = 15

    def GetKey(self):
        out = self.PermutedChoice2.Execute(self.leftKey+self.rightKey)
        self.Rotate()
        return out

    def Rotate(self):
        if self.rotationNumber >= self._BitRotationTable.__len__() or self.rotationNumber < 0:
            raise ("Argument out of range Exception.")
        self.leftKey = self.RotateBits(self.leftKey, -self._GetCurrentRotation())
        self.rightKey = self.RotateBits(self.rightKey, -self._GetCurrentRotation())

        self.rotationNumber -= 1
        if self.rotationNumber < 0:
            self.rotationNumber = 15


class TripleDES:
    def __init__(self, keys):
        if type(keys) is str:
            keys = self.CreateKey(keys)
        if type(keys) is not list or keys.__len__() != 3:
            raise ("keys wrong defined.")
        for key in keys:
            if (type(key) is not BitArray) or (key.__len__() != 64):
                raise ("key wrong defined.")
        self.keys = keys

    @staticmethod
    def __DataCheck(bits64, keys):
        if (type(bits64) is not BitArray) or (bits64.__len__() != 64):
            raise ("bits64 wrong defined.")
        if keys.__len__ == 3:
            raise ("keys wrong defined.")
        for key in keys:
            if (type(key) is not BitArray) or (key.__len__() != 64):
                raise ("key wrong defined.")


    @staticmethod
    def CreateKey(string):
        # String variable (No longer than 21.)
        if string.__len__() > 21:
            raise ("Key too large.")
        key = []
        for i in range(0, 21, 7):
            key.append(DES.CreateKey(string[i:i+7]))
        return key

    def Encrypt(self, bits64):
        TripleDES.__DataCheck(bits64, self.keys)
        out = bits64
        for i in range(0, self.keys.__len__()):
            out = DES(self.keys[i]).Encrypt(out)
        return out

    def Decrypt(self, bits64):
        TripleDES.__DataCheck(bits64, self.keys)
        out = bits64
        for i in range(self.keys.__len__()-1, -1, -1):
            out = DES(self.keys[i]).Decrypt(out)
        return out


class DES:
    def __init__(self, key):
        if type(key) is str:
            key = self.CreateKey(key)
        if (type(key) is not BitArray) or (key.__len__() != 64):
            raise ("key wrong defined.")
        self.key = key

    @staticmethod
    def __DataCheck(bits64, key):
        if (type(bits64) is not BitArray) or (bits64.__len__() != 64):
            raise ("bits64 wrong defined.")
        if (type(key) is not BitArray) or (key.__len__() != 64):
            raise ("key wrong defined.")

    @staticmethod
    def CreateKey(string):
        # String variable (No longer than 7.)
        if string.__len__() > 7:
            raise ("Key too large.")
        string = BitArray(bytes(string, 'utf8'))
        key = BitArray(length=64)
        for i in range(0, string.__len__(), 8):
            key[i:i+8] = string[i:i+7]+BitArray(length=1)
        return key

    def Encrypt(self, bits64):
        DES.__DataCheck(bits64, self.key)
        key_manager = DESEncryptionKeyManager(self.key)
        out = PermutationIP.Execute(bits64)
        l_bits = out[0:32]
        r_bits = out[32:64]
        for i in range(0, 16):
            l_bits, r_bits = DESCell.Encrypt(l_bits, r_bits, key_manager.GetKey())
        out = l_bits + r_bits
        return PermutationIP.Rendo(out)

    def Decrypt(self, bits64):
        DES.__DataCheck(bits64, self.key)
        key_manager = DESDescriptionKeyManager(self.key)
        out = PermutationIP.Execute(bits64)
        l_bits = out[0:32]
        r_bits = out[32:64]
        for i in range(0, 16):
            l_bits, r_bits = DESCell.Decrypt(l_bits, r_bits, key_manager.GetKey())
        out = l_bits + r_bits
        return PermutationIP.Rendo(out)


class DESCell:
    @staticmethod
    def __DataCheck(l_bits, r_bits, key):
        if (type(l_bits) is not BitArray) or (l_bits.__len__() != 32):
            raise ("l_bits wrong defined.")
        if (type(r_bits) is not BitArray) or (r_bits.__len__() != 32):
            raise ("r_bits wrong defined.")
        if (type(key) is not BitArray) or (key.__len__() != 48):
            raise ("key wrong defined.")

    @staticmethod
    def Encrypt(l_bits, r_bits, key):
        DESCell.__DataCheck(l_bits, r_bits, key)
        return r_bits, SBlock.Encrypt(r_bits, key).__xor__(l_bits)

    @staticmethod
    def Decrypt(l_bits, r_bits, key):
        DESCell.__DataCheck(l_bits, r_bits, key)
        return SBlock.Encrypt(l_bits, key).__xor__(r_bits), l_bits


class SBlock:
    @staticmethod
    def __DataCheck(bits32, key):
        if (type(bits32) is not BitArray) or (bits32.__len__() != 32):
            raise ("bits32 wrong defined.")
        if (type(key) is not BitArray) or (key.__len__() != 48):
            raise ("key wrong defined.")

    @staticmethod
    def Encrypt(bits32, key):
        SBlock.__DataCheck(bits32, key)
        out = ExpendingPermutation.Expend(bits32)
        out = out.__xor__(key)
        out = SBoxSubstitution.Reduce(out)
        out = PermutationP.Execute(out)
        return out


class PermutationP:
    __LookUpTable = [
        15, 6, 19, 20, 28, 11, 27, 16,
        0, 14, 22, 25, 4, 17, 30, 9,
        1, 7, 23, 13, 31, 26, 2, 8,
        18, 12, 29, 5, 21, 10, 3, 24]

    @staticmethod
    def __DataCheck(bits32):
        if (type(bits32) is not BitArray) or (bits32.__len__() != 32):
            raise ("bits32 wrong defined.")

    @classmethod
    def Execute(cls, bits32):
        cls.__DataCheck(bits32)
        out = BitArray(length=32)
        for i in range(0, 32):
            out[i] = bits32[cls.__LookUpTable[i]]
        return out


class PermutationIP:
    __LookUpTable = [
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8, 0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
    ]
    __ReversedLookUpTable = [
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25,
        32, 0, 40, 8, 48, 16, 56, 24,
    ]

    @staticmethod
    def __DataCheck(bits64):
        if (type(bits64) is not BitArray) or (bits64.__len__() != 64):
            raise ("bits64 wrong defined.")

    @classmethod
    def Execute(cls, bits64):
        cls.__DataCheck(bits64)
        out = BitArray(length=64)
        for i in range(0, 64):
            out[i] = bits64[cls.__LookUpTable[i]]
        return out

    @classmethod
    def Rendo(cls, bits64):
        cls.__DataCheck(bits64)
        out = BitArray(length=64)
        for i in range(0, 64):
            out[i] = bits64[cls.__ReversedLookUpTable[i]]
        return out


class SBoxSubstitution:
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

    @staticmethod
    def __DataCheck(bites48):
        if (type(bites48) is not BitArray) or (bites48.__len__() != 48):
            raise ("bites48 wrong defined.")

    @classmethod
    def Reduce(cls, bites48):
        cls.__DataCheck(bites48)
        out = BitArray()
        for i in range(0, 8, 1):
            out += SCell.Execute(bites48[i:i + 6], cls.__LookUpTable[i])
        return out


class SCell:
    @staticmethod
    def __DataCheck(bits6):
        if (type(bits6) is not BitArray) or (bits6.__len__() != 6):
            raise ("bits6 wrong defined.")

    @staticmethod
    def Execute(bits6, table):
        SCell.__DataCheck(bits6)
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

    @staticmethod
    def __DataCheck(bits):
        if (type(bits) is not BitArray) or (bits.__len__() != 32):
            raise ("bits wrong defined.")

    @classmethod
    def Expend(cls, bits):
        cls.__DataCheck(bits)
        output = BitArray(length=48)
        for i in range(0, 48, 1):
            output[i] = bits[cls.__LookUpTable[i]]
        return output
