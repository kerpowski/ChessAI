# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 15:00:18 2015

@author: kerpowski
"""

from ChessAI import alphabeta
from ChessLib import Bitboard
import cProfile
import numpy as np
import time

test_mate = '8/6R1/8/8/2n1b3/2k3p1/K7/6r1 w - - 8 101'
foo = Bitboard(test_mate)

t1 = time.time()
prf = cProfile.Profile()
#prf.enable()
a, b = alphabeta(foo, 1, -np.inf, np.inf, 6)
#prf.disable()
#prf.print_stats()
t2 = time.time()

print('Time taken: ', t2-t1)