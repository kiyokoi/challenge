# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 20:10:21 2016

@author: Kiyoko
"""


def matrix(N):
    mat = []
    for i in range(N):
        dice = []
        for j in range(1, 7):
            dice.append(j)
        mat.append(dice)
    return mat

import itertools
import numpy as np


def products(N, M):
    mat = matrix(N)
    all_combo = list(itertools.product(*mat))
    prods = []
    for combo in all_combo:
        tot = 0
        prod = 1
        for x in combo:
            tot += x
            prod *= x
        if tot == M:
            prods.append(prod)
    return prods

print np.mean(products(8, 24))  # 1859.93295417
print np.std(products(8, 24))   # 855.069885347
#print np.mean(products(50, 150))
#print np.std(products(50, 150))
