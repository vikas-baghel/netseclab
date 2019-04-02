import sys
from itertools import islice
from Crypto.Cipher import DES3
from Crypto.Util.strxor import strxor
from time import time
import struct

def ansi_x9_17(V, key):
	'''
	Generator for ansi_x9_17 PRNG
	V: seed. It should be a string of length 8
	key: concat of keys K1 & K2. It should be a string of length 16'''
	des3 = DES3.new(key, DES3.MODE_ECB)
	while True:
		EDT = des3.encrypt(hex(int(time()*10**6))[-8:])
		R = des3.encrypt(strxor(V, EDT))
		V = des3.encrypt(strxor(R, EDT))
		yield int.from_bytes(V,"big")

def main():
	seed = b"vikasbag"
	key = b"mynameisvikasbag"
	limit = 500
	print ('\n'.join([str(i) for i in islice(ansi_x9_17(seed, key), limit)]))


if __name__ == '__main__':
	main()
