import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from matplotlib import pyplot as plt
import sys
import chilkat
# import pyDes

# -------------DES Algorithm---------------
#fixed params
FIXED_IP = [2, 6, 3, 1, 4, 8, 5, 7]
FIXED_EP = [4, 1, 2, 3, 2, 3, 4, 1]
FIXED_IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6]
FIXED_P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
FIXED_P8 = [6, 3, 7, 4, 8, 5, 10, 9]
FIXED_P4 = [2, 4, 3, 1]

S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

#fixed key
KEY = '0111111101'

#permutation function
def permutate(original, fixed_key):
    return ''.join(original[i - 1] for i in fixed_key)

#return left half of 8-bit block
def left_half(bits):
    return bits[:len(bits)//2]

#return right half of 8-bit block
def right_half(bits):
    return bits[len(bits)//2:]

#shifts of key
def shift(bits):
    rotated_left_half = left_half(bits)[1:] + left_half(bits)[0]
    rotated_right_half = right_half(bits)[1:] + right_half(bits)[0]
    return rotated_left_half + rotated_right_half

#key of round 1
key1=permutate(shift(permutate(KEY, FIXED_P10)), FIXED_P8)

#key of round 2
key2=permutate(shift(shift(shift(permutate(KEY, FIXED_P10)))), FIXED_P8)

#XOR function
def xor(bits, key):
    return ''.join(str(((bit + key_bit) % 2)) for bit, key_bit in
                   zip(map(int, bits), map(int, key)))

#S-box lookup
def lookup_in_sbox(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return '{0:02b}'.format(sbox[row][col])

#f(p,k)
def f_k(bits, key):
    L = left_half(bits)
    R = right_half(bits)
    bits = permutate(R, FIXED_EP)
    bits = xor(bits, key)
    bits = lookup_in_sbox(left_half(bits), S0) + lookup_in_sbox(right_half(bits), S1)
    bits = permutate(bits, FIXED_P4)
    return xor(bits, L)

#encrypt
def encrypt(plain_text):
    bits = permutate(plain_text, FIXED_IP)
    temp = f_k(bits, key1)
    bits = right_half(bits) + temp
    bits = f_k(bits, key2)
    return(permutate(bits + temp, FIXED_IP_INVERSE))

#decrypt
'''def decrypt(cipher_text):
    bits = permutate(cipher_text, FIXED_IP)
    temp = f_k(bits, key2)
    bits = right_half(bits) + temp
    bits = f_k(bits, key1)
    return(permutate(bits + temp, FIXED_IP_INVERSE))
'''
#ECB Mode
def ECB(pt):
    l=len(pt)
    a=[pt[k:k+8] for k in range(0, l, 8)]
    ct=''.join(encrypt(i) for i in a)
    res=[]
    for i in range(256):
        row=[]
        for j in range(256):
            if ct[256*i+j]=='0':
                row.append(0)
            else:
                row.append(255)
        res.append(row)
    return res

#CBC Mode
def CBC(pt):
    iv='10010011'
    l=len(pt)
    a=[pt[k:k+8] for k in range(0, l, 8)]
    ctl=[]
    for i in a:
        temp=xor(i,iv)
        ctl.append(temp)
        iv=temp
    ct=''.join(ctl)
    res=[]
    for i in range(256):
        row=[]
        for j in range(256):
            if ct[256*i+j]=='0':
                row.append(0)
            else:
                row.append(255)
        res.append(row)
    return res

im=cv2.imread('test3.jpg')
img = cv2.imread('test3.jpg',0)
# img = cv2.resize(img, (1000,600))
ret,img = cv2.threshold(img,127,1,cv2.THRESH_BINARY)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
resized = cv2.resize(img,(128,128), cv2.INTER_LINEAR)
# print (img)
# plt.imsave('img2.jpg',np.array(img).reshape(1080,1920), cmap=cm.gray)
c=img.flatten()
print(c)

istring=""
for digit in c:
    istring += str(digit)

plt.subplot(1, 3, 1)
plt.imshow(im)
plt.title("Original Image")

plt.subplot(1, 3, 2)
plt.imshow(ECB(istring))
plt.title("ECB Mode")

plt.subplot(1, 3, 3)
plt.imshow(CBC(istring))
plt.title("CBC Mode")

plt.show()

