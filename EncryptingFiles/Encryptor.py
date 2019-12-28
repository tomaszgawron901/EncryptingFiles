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
			raise("l_bits wrong defined.")
		if (type(r_bits) is not BitArray) or (r_bits.__len__() != 32):
			raise("r_bits wrong defined.")
		if (type(key) is not BitArray) or (key.__len__() != 32):
			raise("key wrong defined.")

		return r_bits, l_bits


class SBlock:
	@staticmethod
	def Encrypt(bits32, key):
		if (type(bits32) is not BitArray) or (bits32.__len__() != 32):
			raise("bits32 wrong defined.")
		if (type(key) is not BitArray) or (key.__len__() != 48):
			raise("key wrong defined.")
		return BitArray(np.bitwise_xor(ExpendingPermutation.Expend(bits32), key))


class ExpendingPermutation:
	__LookUpTable = [
		31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10,
		11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20,
		21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0
	]

	@staticmethod
	def Expend(bits):
		if (type(bits) is not BitArray) or (bits.__len__() != 32):
			raise("bits wrong defined.")
		output = BitArray('0x000000000000')
		for i in range(0, 48, 1):
			output[i] = bits[ExpendingPermutation.__LookUpTable[i]]
		return output
