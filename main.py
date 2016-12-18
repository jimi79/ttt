#!/usr/bin/python3

import copy
import importlib
import numpy
import random
import ttt

def init_ai(name): 
	ai=ttt.AI()
	ai.random=False
	ai.name=name 
	ai.verbose=True
	ai.filename="%s_ttt_ql.tmp" % name
	ai.logfilename="%s_ttt_ql.log" % name 
	ai.win=1000 # define the value at which it's a win 
	return ai 

zeros=[0,0,0,0,0,0,0,0,0]
wins=[]
wins.append([1,1,1,0,0,0,0,0,0])
wins.append([0,0,0,1,1,1,0,0,0])
wins.append([0,0,0,0,0,0,1,1,1])
wins.append([1,0,0,1,0,0,1,0,0])
wins.append([0,1,0,0,1,0,0,1,0])
wins.append([0,0,1,0,0,1,0,0,1])
wins.append([1,0,0,0,1,0,0,0,1])
wins.append([0,0,1,0,1,0,1,0,0])


alice=init_ai("alice")
bob=init_ai("bob") 
all_actions=list(range(1,11)) 
short_display=False

def print_game(alice, bob):
	c=["X" if alice[i]==1 else "O" if bob[i]==1 else " " for i in range(9)]
	if short_display: 
		print("%s%s%s" % (c[0],c[1],c[2]))
		print("%s%s%s" % (c[3],c[4],c[5]))
		print("%s%s%s" % (c[6],c[7],c[8]))
	else: 
		print("%s│%s│%s" % (c[0],c[1],c[2]))
		print("─┼─┼─")
		print("%s│%s│%s" % (c[3],c[4],c[5]))
		print("─┼─┼─")
		print("%s│%s│%s" % (c[6],c[7],c[8]))

def print_game_from_int(integer):
	a=ttt.integer_to_array(integer)
	b=a[0:9]
	c=a[9:19]
	print_game(b,c) 

def print_history(array, winner=None):
	for i in range(3):
		s=""
		s2=""
		for h in array:
			a=h[i*3:(i*3)+3]
			b=["X" if i==1 else "O" if i==2 else "?" if i!=0 else " " for i in a]
			s+="%s│%s│%s  " % (b[0], b[1], b[2])
			s2+="─┼─┼─  "
		print(s)
		if i==1:
			if not winner is None:
				s2+=" winner:%s" % winner
		if i < 2:
			print(s2)

def print_history_points(array):
	s=""
	for i in array:
		s2=str(i)
		while len(s2)<7:
			s2=" %s" % s2
		s+=s2
	print(s) 

def list_or(list1,list2):
	return [a or b for a,b in zip(list1,list2)]

def get_available_actions(busy):
	l=[1-i for i in busy]
	return [i for i in range(len(l)) if l[i]==1]

def is_win(list_):
	for i in wins:
		if sum(i)==sum([a*b for a,b in zip(list_,i)]):
			return True
	return False

def is_tie(board, board2): 
	if sum(board)+sum(board2)==9:
		return True
	else:
		return False

def test_play(int_):
	b=ttt.integer_to_array(int_)
	board=b[0:9]
	board2=b[9:18]
	return one_move(alice, alice, board, board2, verbose=True)	

def one_move(player, player2, board, board2, verbose=False):
	old_board=board+board2
	old_board2=board2+board
	possible_actions=get_available_actions(list_or(board, board2))
	player.init_status(board+board2, possible_actions) 
	player.init_status(board2+board, possible_actions) 
	#print(ttt.array_to_integer(old_board))
	move=player.play(board + board2, possible_actions, verbose=verbose) # those are lists 
	board[move]=1
	new_board=board+board2
	new_board2=board2+board
	win=is_win(board+board2)	
	tie=False
	if not win:
		tie=is_tie(board, board2)
	if win:
		player.learn_points(board+board2, 2)
		player.learn_points(board2+board, -2)
	if tie:
		player.learn_points(board+board2, -1)
		player.learn_points(board2+board, -1)
	if verbose:
		print_game(board,board2)
	player.learn_path(old_board, move, new_board)
	player.learn_path_opponent(old_board2, move, new_board2)
	return win, tie, move

# should i learn it it can loose ? yeah of course

def one_game(history=False, verbose=False): 
	history_moves=[]
	history_points=[]
	history_points_o=[]
	board_a=copy.copy(zeros)
	board_b=copy.copy(zeros) 
	end_of_game=False
	winner=None
	while not end_of_game:
		win, tie, move=one_move(alice, alice, board_a, board_b, verbose=verbose)
		if win:
			winner="alice"
		h=[a+b*2 for a,b in zip(board_a, board_b)]
		history_points.append(ttt.array_to_integer(board_a+board_b))
		history_points_o.append(ttt.array_to_integer(board_b+board_a))
		history_moves.append(h)
		if not win and not tie:
			win, tie, move=one_move(alice, alice, board_b, board_a, verbose=verbose)
			if win:
				winner="bob"
			h=[a+b*2 for a,b in zip(board_a, board_b)]
			history_points.append(ttt.array_to_integer(board_a+board_b))
			history_points_o.append(ttt.array_to_integer(board_b+board_a))
			history_moves.append(h)
		end_of_game=win or tie

	if history:
		print_history(history_moves)
		print_history_points(history_points)
		print_history_points(history_points_o)
	return winner

def multiples_games(cpt, history=False, verbose=False, display=100, reset=1000):
	a=0
	print("%d %%" % a, end="", flush=True)
	totalice=0
	totbob=0
	tottie=0
	tot=0
	cdisplay=0
	if display>reset:
		reset=display
	for i in range(cpt): 
		if cdisplay==display:
			print("\033[0Galice %.2f bob %.2f tie %.2f cpt %d" % (totalice/tot*100, totbob/tot*100, tottie/tot*100, tot))
			cdisplay=0
		if tot == reset:
			print("\033[0Kreset")
			totalice=0
			totbob=0
			tottie=0
			tot=0
		tot+=1
		cdisplay+=1
		b=int(i/cpt*100)
		if b!=a:
			print("\033[0G%d %%" % b, end="", flush=True)
			a=b
		winner=one_game(history=history, verbose=verbose)
		if winner=="alice":
			totalice+=1
		else:
			if winner=="bob":
				totbob+=1
			else:
				tottie+=1 
	print("\033[0K\033[0G100%")
	alice.save()
	print("saved")

alice.try_load()
