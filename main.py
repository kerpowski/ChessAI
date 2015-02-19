# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 22:58:32 2015

@author: kerpowski
"""
import sys
import numpy as np

from ChessLib import Move, Bitboard
from ChessAI import alphabeta
from Dispatcher import Dispatcher

@Dispatcher
class Game(object):
    def __init__(self):
        self.board = Bitboard()
        pass
    
    def handle_gameover(board):
        if board.is_checkmate():
            if board.turn == 0:
                print('Black wins')
            else:
                print('White wins')
        
        if board.is_stalemate():
            print('Stalemate')
            
        return board.is_game_over()            
    
    @Dispatcher.dispatch_method(None)
    @Dispatcher.dispatch_method('help') 
    @Dispatcher.dispatch_method('h')   
    def print_help(self, *args, **kwargs):
        print('Super Helpful!!!')
        #JAKE: put this in the dispatch markup... stupid to maintain this
        print('Available commands... figure out details yourself for now')
        for c in Game.instance_map.keys():
            print(c)
        
        
    @Dispatcher.dispatch_method('move')
    @Dispatcher.dispatch_method('m')   
    def make_move(self, *args, **kwargs):
        print('Moving!')
        if len(args) == 1:
            m = Move.from_uci(args[0])
            if m not in self.board.legal_moves:
                print(args[0] + ' is not a legal move.  Type "list" to view legal moves')
            else:
                self.board.push(m)
                if Game.handle_gameover(self.board):
                    return True
                    
                # ugly heuristic for determining search depth based off of piece count
                c = sum(1 for _ in (x for x in self.board.pieces if x != 0))
                depth = 3
                if c <= 6:
                    depth = 5
                elif c <= 9:
                    depth = 4
                    
                score, main_line = alphabeta(self.board, 1, -np.inf, np.inf, depth)
                if len(main_line) == 0:
                    print("ummm, I don't know how to say this but our robot got a bit confused")
                    print("You win by default!")
                    return True
                self.board.push(main_line[0])
                
                if Game.handle_gameover(self.board):
                    return True
                    
                self.print_board()
        else:
            #JAKE: move this into dispatch handling?
            print('Move command takes 1 argument')
        
    @Dispatcher.dispatch_method('undo')
    @Dispatcher.dispatch_method('u')
    def undo(self, *args, **kwargs):
        print('Undo!')
        self.board.pop()
        self.board.pop()
        self.print_board()
    
    @Dispatcher.dispatch_method('board')
    @Dispatcher.dispatch_method('b')
    @Dispatcher.dispatch_method('print')
    @Dispatcher.dispatch_method('p')
    def print_board(self, *args, **kwargs):
        print('Board!')
        print(self.board)
    
    @Dispatcher.dispatch_method('list')
    @Dispatcher.dispatch_method('l')
    def list_moves(self, *args, **kwargs):
        print('Legal Moves!')        
        for m in self.board.legal_moves:
            print(m)
    
    @Dispatcher.dispatch_method('new')
    def new_game(self, *args, **kwargs):
        print('New Game!')
        self.board = Bitboard()
        
    
if __name__ == '__main__':
    print('Simple Chess AI v1.0')
    g = Game()
    g.print_board()
    print()
    
    while True:
        print('Enter command:  ')
        line = sys.stdin.readline()
        if g.dispatch(line) == True:
            break
        print() 
        
    