
from scipy.stats import norm

lcg = []
ansi=[]
bbs=[]

def generate_lcg(num_iterations, lcg=[]):
    x_value = 15
    a = 3
    c = 0
    m = 31

    counter = 0

    while counter < num_iterations:
        x_value = (a * x_value + c) % m
        lcg.append(x_value / m)
        counter = counter + 1


#########----ANSI9.17------########

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
        EDT = des3.encrypt(hex(int(time() * 10 ** 6))[-8:])
        R = des3.encrypt(strxor(V, EDT))
        V = des3.encrypt(strxor(R, EDT))
        # print(type(int.from_bytes(V, "big")))
        yield int.from_bytes(V, "big")


def support_ansi_x9_17(number_observations):
    seed = b"vikasbag"
    key = b"mynameisvikasbag"
    limit = number_observations
    x_value =[]
    m=2**32
    for i in islice(ansi_x9_17(seed, key), limit):
        x_value.append(i/m)
    return x_value
    # print(type(x_value))
    # x_value
    # m = (2 ** 32)
    # lcg.append(str(x_value / m))

################------------BBS-----------##############
from itertools import islice

def bbs_util(s, p=19, q=3):
	assert p%4==3 and q%4==3
	n = p*q
	x = (s*s) % n
	while True:
		x = (x*x) % n
		yield x

def bbs_f(num):
    # s, limit = [int(x) for x in sys.argv[1:]]
    s = 101355
    limit = num
    ans =[]
    for i in islice(bbs_util(s), limit):
        ans.append(i)
    return ans


def divide_into_10_equal_subdivisions_and_count(lcg):
    subdivisions = {"1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0,
                    "10": 0}
    for num in lcg:
        num = float(num)
        if num < 0.1:
            subdivisions["1"] += 1
        elif num < 0.2:
            subdivisions["2"] += 1
        elif num < 0.3:
            subdivisions["3"] += 1
        elif num < 0.4:
            subdivisions["4"] += 1
        elif num < 0.5:
            subdivisions["5"] += 1
        elif num < 0.6:
            subdivisions["6"] += 1
        elif num < 0.7:
            subdivisions["7"] += 1
        elif num < 0.8:
            subdivisions["8"] += 1
        elif num < 0.9:
            subdivisions["9"] += 1
        elif num < 1.0:
            subdivisions["10"] += 1

    return subdivisions


def chi_sq_uniformity_test(data_set, confidence_level, num_samples):
    chi_sq_value = 0.0
    degrees_of_freedom = num_samples - 1

    expected_val = num_samples / 10

    for observed_val in data_set:
        chi_sq_value += (pow((expected_val - data_set[observed_val]), 2) / expected_val)

    return chi_sq_value


def chi_sq_significance_test(chi_sq, signif_level):
    crit_value = 0.0
    result = "chi squared test passed"

    if signif_level == 0.8:
        crit_value = 10118.8264
    elif signif_level == 0.90:
        crit_value = 10181.6616
    elif signif_level == 0.95:
        crit_value = 10233.7489
    else:
        print("**Invalid Significance Level for Chi Sq***")

    if chi_sq > crit_value:
        result = "chi squared test failed"

    print("Print Significance Level: " + str(signif_level))
    print("Chi Sq: " + str(chi_sq))
    print("Crit Value: " + str(crit_value))
    print("Result is: " + result)
    print("....................................")

    return result

def kol_smir(arr, n):
    m = sum(arr) / n
    st = (sum([(i - m) ** 2 for i in arr]) / (n - 1)) ** 0.5
    print(m, st)
    arr = [float((i - m) / st) for i in arr]
    arr1 = [float(norm.cdf(i, 0, 1)) for i in arr]
    arr1.sort()

    arr2 = [float(i / n) for i in range(1, n + 1)]

    obs_val = max([abs(arr1[i] - arr2[i]) for i in range(n)])

    critical_val = float(1.36 / (n ** 0.5))
    print(obs_val, critical_val)
    if (obs_val < critical_val):
        print("K.S test passed")
    else:
        print("K.S test failed")

def run_tests(number_observations,arr=[]):
    data_points = divide_into_10_equal_subdivisions_and_count(arr)
    chi_sq_result = chi_sq_uniformity_test(data_points, 0, number_observations)
    chi_sq_significance_test(chi_sq_result, 0.8)
    chi_sq_significance_test(chi_sq_result, 0.9)
    chi_sq_significance_test(chi_sq_result, 0.95)

    kol_smir(arr,len(arr))

def main():
    number_observations = 1000
    print("\n\n<-------------------LCG------------------->")
    generate_lcg(number_observations, lcg)
    run_tests(number_observations,lcg)


    print("\n\n<-----------------ANSI_x9.17------------->")
    ansi=support_ansi_x9_17(number_observations)
    run_tests(number_observations, ansi)

    print("\n\n<---------------------BBS----------------->")
    bbs = bbs_f(number_observations)
    print(bbs[:10])
    print(type(bbs[0]))
    run_tests(number_observations,bbs)


main()
