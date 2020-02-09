"""
This service can be provided by any node, and the one doing so will get the
appropriate remuneration/incentive for its job
"""

import math
from functools import reduce
from operator import mul


def is_prime_number(i):
    for j in range(2, i):
        if not (i % j):
            return False
    return True


def factors(n):
    facts = []
    for c in range(2, n):
        if n % c == 0:
            facts.append(c)
    return facts
    # this line was for prime factors only. but what's the fun in that?
    # and is_prime_number(c)


def process_string(s):
    Map = {"a":3, "B":4, "c":5, "D":6, "e":7, "F":8, "g":9, "H":10, "i":11, "J":12, "k":13, "L":14, "m":15, "N":16, "o":17, "P":18, "q":19,
           "R":20, "s":21, "T":22, "u":23, "V":24, "w":25, "X":26, "y":27, "Z":28,
           "A":29, "b":30, "C":31, "d":32, "E":33, "f":34, "G":35, "h":36, "I":37, "j":38, "K":39, "l":40, "M":41, "n":42, "O":43, "p":44,
           "Q":45, "r":46, "S":47, "t":48, "U":49, "v":50, "W":51, "x":52, "Y":53, "z":54,
           "0":55, "1":56, "2":57, "3":58, "4":59, "5":60, "6":61, "7":62, "8":63, "9":64,
           "@":65, "-":66, "_":67, "&":68, "$":69, "|": 70, "<": 71, ">": 72, "~": 73}

    string = s[:]
    # the sum of all characters in the string
    S = sum([Map[c] for c in string])
    # the product of those characters in the string whose index is odd 
    P = reduce(mul, [Map[string[c]] for c in range(len(string)) if c % 2 != 0], 1)

    # print(S,": ", factors(S), "\n", P, ": ", factors(P))
    common = list(set(factors(S) + factors(P)))
    print(common)
    return common


def get_factors(username, password):
    # factors for username
    u_factors = process_string(username)
    u_factors.sort()
    u_factor_one = u_factors[math.floor(len(u_factors)/2) - 1]
    u_factor_two = u_factors[math.floor(len(u_factors)/2)]

    # factors for password
    p_factors = process_string(password)
    p_factors.sort()
    p_factor_final = p_factors[math.floor(len(p_factors)*0.65)-1]

    print("Respective factors for username and password are: ", u_factors, p_factors)
    print("\nUser factors: ", u_factor_one,u_factor_two, "\nPass factor: ", p_factor_final)
    return [u_factor_one, u_factor_two, p_factor_final]
