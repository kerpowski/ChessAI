# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 15:24:16 2015

@author: kerpowski
"""

from ChessAI import alphabeta, position_bonus_late
from ChessLib import Bitboard, bit_count
import ChessLib
import numpy as np
import time

def test_white_mate_in_three():
    test_mate = 'k7/8/8/1Q6/2K5/8/8/8 w - - 11 11'
    foo = Bitboard(test_mate)
    a, b = alphabeta(foo, 1, -np.inf, np.inf, 5)
    print(a, b)


def test_avoid_stalemate():
    test_mate = '8/k7/8/1Q6/2K5/8/8/8 b - - 10 10'
    foo = Bitboard(test_mate)
    a, b = alphabeta(foo, 1, -np.inf, np.inf, 2)
    print(a, b)

def test_avoid_stalemate2():
    test_mate = 'k7/8/8/1Q6/2K5/8/8/8 w - - 11 11'
    foo = Bitboard(test_mate)
    a, b = alphabeta(foo, 1, -np.inf, np.inf, 2)
    print(a, b)

def test_mate_in_three():
    test_mate = '8/k7/8/1Q6/2K5/8/8/8 b - - 10 10'
    foo = Bitboard(test_mate)
    a, b = alphabeta(foo, 1, -np.inf, np.inf, 5)
    print(a, b)

def test_mate_in_one():
    test_mate_in_one = '8/k1K5/8/1Q6/8/8/8/8 b - - 10 10'
    foo = Bitboard(test_mate_in_one)
    a, b = alphabeta(foo, 1, -np.inf, np.inf, 1)
    print(a, b)
    
def test_long_mate():
    test_mate = '8/k7/8/1Q6/8/8/2K5/8 b - - 10 10'
    foo = Bitboard(test_mate)
    a, b = alphabeta(foo, 1, -np.inf, np.inf, 5)
    print(a, b)

def test_rook_mate():
    test_mate = '8/k7/8/1R6/8/8/2K5/8 b - - 0 0'
    foo = Bitboard(test_mate)
    for i in range(100):
        a, b = alphabeta(foo, 1, -np.inf, np.inf, 3)
        if len(b) > 0:
            foo.push(b[0])
        else: 
            break
    
    #assert    
    foo.is_checkmate() and foo.turn == ChessLib.BLACK
    
def test_bishop_and_pawn_mate():
    test_mate = '8/k7/8/1B6/8/8/1P6/7K b - - 10 10'
    foo = Bitboard(test_mate)
    for i in range(100):
        a, b = alphabeta(foo, 1, -np.inf, np.inf, 3)
        if len(b) > 0:
            foo.push(b[0])
        else: 
            break
  
    #assert    
    foo.is_checkmate() and foo.turn == ChessLib.BLACK
    
test_mate = '8/k7/8/1B6/8/8/1P6/7K b - - 10 10'
test_mate = '8/6R1/8/8/2n1b3/2k3p1/K7/6r1 w - - 8 101'
foo = Bitboard(test_mate)
a = 0
b = []
for i in range(100):
    a, b = alphabeta(foo, 1, -np.inf, np.inf, 5)
    if len(b) > 0:
        foo.push(b[0])
        print(i, a, b)
        print(foo)
    else:
        break

def animate_moves(start, moves):
    print(start)
    for m in moves:
        time.sleep(0.5)
        start.push(m)
        print(start)