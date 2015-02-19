# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 16:52:35 2015

@author: kerpowski
"""

cimport cython
cimport numpy as np
import numpy as np

cdef class Move(object):
    cdef public unsigned long long from_square
    cdef public unsigned long long to_square
    cdef public unsigned long long promotion

#cdef unsigned long long* BB_PAWN_ATTACKS_WHITE = [1, 2, 3]

cpdef inline unsigned int rank_index(unsigned int square)
cpdef inline unsigned int file_index(unsigned int square)

cpdef inline unsigned long long shift_up(unsigned long long b)
cpdef inline unsigned long long shift_2_up(unsigned long long b)
cpdef inline unsigned long long shift_right(unsigned long long b)
cpdef inline unsigned long long shift_2_right(unsigned long long b)
cpdef inline unsigned long long shift_left(unsigned long long b)
cpdef inline unsigned long long shift_2_left(unsigned long long b)
cpdef inline unsigned long long shift_up_left(unsigned long long b)
cpdef inline unsigned long long shift_up_right(unsigned long long b)

    
cdef public unsigned long long BB_RANK_1
cdef public unsigned long long BB_RANK_2
cdef public unsigned long long BB_RANK_3
cdef public unsigned long long BB_RANK_4
cdef public unsigned long long BB_RANK_5
cdef public unsigned long long BB_RANK_6
cdef public unsigned long long BB_RANK_7
cdef public unsigned long long BB_RANK_8

cdef public unsigned long long BB_A1, BB_B1, BB_C1, BB_D1, BB_E1, BB_F1, BB_G1, BB_H1
cdef public unsigned long long BB_A2, BB_B2, BB_C2, BB_D2, BB_E2, BB_F2, BB_G2, BB_H2
cdef public unsigned long long BB_A3, BB_B3, BB_C3, BB_D3, BB_E3, BB_F3, BB_G3, BB_H3
cdef public unsigned long long BB_A4, BB_B4, BB_C4, BB_D4, BB_E4, BB_F4, BB_G4, BB_H4
cdef public unsigned long long BB_A5, BB_B5, BB_C5, BB_D5, BB_E5, BB_F5, BB_G5, BB_H5
cdef public unsigned long long BB_A6, BB_B6, BB_C6, BB_D6, BB_E6, BB_F6, BB_G6, BB_H6
cdef public unsigned long long BB_A7, BB_B7, BB_C7, BB_D7, BB_E7, BB_F7, BB_G7, BB_H7
cdef public unsigned long long BB_A8, BB_B8, BB_C8, BB_D8, BB_E8, BB_F8, BB_G8, BB_H8

cdef public unsigned int CASTLING_NONE
cdef public unsigned int CASTLING_WHITE_KINGSIDE
cdef public unsigned int CASTLING_BLACK_KINGSIDE
cdef public unsigned int CASTLING_WHITE_QUEENSIDE
cdef public unsigned int CASTLING_BLACK_QUEENSIDE
cdef public unsigned int CASTLING_WHITE
cdef public unsigned int CASTLING_BLACK
cdef public unsigned int CASTLING 

#==============================================================================
# cdef public list BB_SQUARES
# cdef public list SQUARES_L90
# cdef public list SQUARES_R45
# cdef public list SQUARES_L45
# cdef public list BB_PAWN_ATTACKS
# cdef public list POLYGLOT_RANDOM_ARRAY
#==============================================================================

cdef class Bitboard(object):
    cdef public unsigned long long pawns
    cdef public unsigned long long knights
    cdef public unsigned long long bishops
    cdef public unsigned long long rooks 
    cdef public unsigned long long queens 
    cdef public unsigned long long kings

    cdef public list occupied_co
    cdef public unsigned long long occupied 
    cdef public unsigned long long occupied_l90
    cdef public unsigned long long occupied_l45
    cdef public unsigned long long occupied_r45 
    
    cdef public unsigned long long turn
    cdef public unsigned long long fullmove_number
    cdef public unsigned long long ep_square
    cdef public unsigned long long halfmove_clock
    cdef public unsigned long long castling_rights
    cdef public unsigned long long incremental_zobrist_hash 
    
    cdef public list king_squares
    cdef public list pieces
    cdef public PseudoLegalMoveGenerator pseudo_legal_moves  
    cdef public LegalMoveGenerator legal_moves  
    cdef public halfmove_clock_stack
    cdef public captured_piece_stack 
    cdef public castling_right_stack 
    cdef public ep_square_stack 
    cdef public move_stack 
    
    cdef public transpositions
    cdef public unsigned long long board_zobrist_hash(self, array=*)
    cdef public unsigned long long zobrist_hash(self, array=*)
    cpdef public unsigned long long attacker_mask(self, unsigned long long color, unsigned long long square)
    cpdef public unsigned long long rook_attacks_from(self, unsigned long long square)
    cpdef public unsigned long long bishop_attacks_from(self, unsigned long long square)
    cpdef bint is_attacked_by(self, unsigned long long color, unsigned long long square)
    
cdef class PseudoLegalMoveGenerator(object): 
    cdef public bitboard
    
cdef class LegalMoveGenerator(object):
    cdef public bitboard
    
