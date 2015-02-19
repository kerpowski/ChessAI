# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 00:36:23 2015

@author: kerpowski
"""

import numpy as np
import ChessLib
import cProfile
import copy
import time
from ChessLib import bit_count, rank_index, file_index
import cython

def debug_print(*x):
    if False:
        print(*x)

def current_material(board, color):
    total = 0
    mask = board.occupied_co[color]
    total += 9 * bit_count(mask & board.queens)
    total += 5 * bit_count(mask & board.rooks)
    total += 3 * bit_count(mask & board.bishops)
    total += 3 * bit_count(mask & board.knights)
    total += 1 * bit_count(mask & board.pawns)
    
    return total

def get_control_value(x):
    if x > 1:
        return 2.1
    elif x > 0:
        return 1
    elif x < -1:
        return -1.3
    elif x < 0:
        return -1.1
    else:
        return 0

position_weights =  (
    1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 2, 2, 2, 2, 1, 1,
    1, 1, 2, 3, 3, 2, 1, 1,
    1, 1, 2, 3, 3, 2, 1, 1,
    1, 1, 2, 2, 2, 2, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1    
)

mask_square_map = {1 << i:i for i in range(64)}

king_position_bonus_late = (
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 13, 13, 13, 13, 0, 0,
    0, 0, 13, 30, 30, 13, 0, 0,
    0, 0, 13, 30, 30, 13, 0, 0,
    0, 0, 13, 13, 13, 13, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0
)


def position_bonus_late(board, color, our_material, opp_material):
    our_king = mask_square_map[board.kings & board.occupied_co[color]]
    opp_king = mask_square_map[board.kings & board.occupied_co[color ^ 1]]
    bonus = king_position_bonus_late[our_king] - king_position_bonus_late[opp_king] 
    if our_material - opp_material > 3:
        king_rank_distance = abs(rank_index(our_king) - rank_index(opp_king))
        king_file_distance = abs(file_index(our_king) - file_index(opp_king))
        dist = min(king_rank_distance, king_file_distance) + abs(king_rank_distance - king_file_distance)
        bonus += 200 * (1 - ((dist**4)/(7**4)))
    
    return bonus
    
def position_value(board, color, our_material, opp_material):
    our_attacks = [position_weights[x] * bit_count(board.attacker_mask(color, x)) for x in range(64)]    
    opp_attacks = [position_weights[x] * bit_count(board.attacker_mask(color ^ 1, x)) for x in range(64)]    
    total = sum(map(lambda x: get_control_value(x[0] - x[1]), zip(our_attacks, opp_attacks)))
    
    if our_material < 12:
        total += position_bonus_late(board, color, our_material, opp_material)        
    return 0.01 * total

mmax_calls = 0
def minimax(board, sign, depth): 
    # Slow minimax implementation.  Here only for testing of the alphabeta version
    global mmax_calls 
    indent = ''.join(' ' for x in range(depth))
    if sign == 1:
        debug_print(indent, "maximizing")
    else:
        debug_print(indent, "minimizing")
        
    current_max = -np.inf
    chain = []
    new_board = copy.deepcopy(board)
    for m in board.pseudo_legal_moves:        
        item_max = -np.inf
        chain_max = []
        if depth > 0:
            new_board.push(m)
            item_max, chain_max = minimax(new_board, -sign, depth-1)
            new_board.pop()
        else:
            item_max = current_material(new_board, int((sign+1)/2))
            mmax_calls += 1        
            
        item_max = -item_max
        if item_max > current_max:
            current_max = item_max
            chain = [m] + chain_max
            
        debug_print(indent, current_max)
    
    #handle stalemate condition 
    if len(chain) == 0:
        current_max = 0
    return current_max, chain
    
ab_calls = 0
@cython.ccall 
@cython.locals(alpha=cython.float, 
               beta=cython.float, 
               sign=cython.int, 
               depth=cython.int,
               current_max=cython.float,
               item_max=cython.float)
def alphabeta(board, sign, alpha, beta, depth):
    global ab_calls 
    indent = ' ' * depth
    if sign == 1:
        debug_print(indent, "maximizing", alpha, beta)
    else:
        debug_print(indent, "minimizing", alpha, beta)
        
    current_max = -np.inf
    chain = []
    new_board = board
    turn = board.turn
    
    for m in board.pseudo_legal_moves:   
        debug_print(depth, m)
        item_max = -np.inf
        chain_max = []
        if alpha >= beta:
            debug_print(indent, m, "pruning", alpha, beta)
            break
        
        try:
            new_board.push(m)
        except:
            print(new_board, m)
        
        if new_board.was_into_check():
            new_board.pop()
            continue

        #print(depth, m)
        if new_board.is_checkmate():
            #big number but less than np.inf... otherwise it'll get pruned
            item_max = 10000
        else:
            if depth > 0:            
                item_max, chain_max = alphabeta(new_board, -sign, -beta, -alpha, depth-1)
                item_max = -item_max
            else:
                our_material = current_material(new_board, turn)
                opp_material = current_material(new_board, turn ^ 1)
                material_value = our_material - opp_material
                item_max = material_value
                item_max += position_value(new_board, turn, our_material, opp_material)
                ab_calls += 1
        
        if board.can_claim_draw():
            item_max = max(item_max, 0)
            
        new_board.pop()
        
        if item_max > current_max:
            current_max = item_max
            chain = [m] + chain_max
            
        alpha = max(item_max, alpha)
        debug_print('current chain: ', chain)
        debug_print(indent, m, current_max, alpha, beta)
    
    # deal with stalemate by no moves
    if len(chain) == 0:
        current_max = 0
        
    return current_max, chain 

 
if __name__ == '__main__':
    t1 = time.time()
    prf = cProfile.Profile()
    #prf.enable()
    
    current_board = ChessLib.Bitboard()
    current_color = 1
    
    for i in range(200):
        a, main_line = alphabeta(current_board, current_color, -np.inf, np.inf, 3)
        current_board.push(main_line[0])
        current_color = -current_color
       
        print(i)
        print(current_board)
        if current_board.is_checkmate():
            break
        
    print(current_board.move_stack)
    
    #prf.disable()
    #prf.print_stats()
    t2 = time.time()
    print("time taken: ", t2-t1)
    #print(m, c)
    #print(a, c2)
    
    
    
