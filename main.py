#!/usr/bin/python3

import copy
import importlib
import itertools
import math
import numpy
import pdb
import random
import sys
import ttt
import pydoc

def init_ai(name): 
	ai=ttt.AI()
	ai.random=True
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

def print_board_array(alice, bob):
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

def print_board_int(integer):
	a=ttt.integer_to_array(integer)
	b=a[0:9]
	c=a[9:19]
	print_board_array(b,c) 

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
	return one_move(alice, board, board2)	

def one_move(player, board, board2):
	old_board=board+board2
	old_board_b=board2+board
	available_actions=get_available_actions(list_or(board, board2))

	player.init_status(list(board+board2), available_actions) 
	player.init_status(list(board2+board), available_actions) 

	#print(ttt.array_to_integer(old_board))
	move=player.play(board + board2, available_actions) # those are lists 
	board[move]=1
	new_board=board+board2
	new_board_b=board2+board
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
	player.learn_path(old_board, move, new_board)
	player.learn_path_opponent(old_board_b, move, new_board_b)
	return win, tie, move

# should i learn it it can loose ? yeah of course

def one_game(history=False, verbose=False): 
	alice.verbose=verbose
	#alice.calculate(0) # ok, so here we calculate everythg
	history_moves=[]
	history_boards=[]
	history_points=[]
	history_points_o=[]
	board_a=copy.copy(zeros)
	board_b=copy.copy(zeros) 
	end_of_game=False
	winner=None
	while not end_of_game:
		if verbose:
			print_board_array(board_a, board_b)
			print("alice plays")
		win, tie, move=one_move(alice, board_a, board_b)
		history_moves.append(move)
		if win:
			winner="alice"
		h=[a+b*2 for a,b in zip(board_a, board_b)]
		history_points.append(ttt.array_to_integer(board_a+board_b))
		history_points_o.append(ttt.array_to_integer(board_b+board_a))
		history_boards.append(h)
		if not win and not tie:
			if verbose:
				print_board_array(board_a, board_b)
				print("bob plays")
			win, tie, move=one_move(alice, board_b, board_a)
			history_moves.append(move)
			if win:
				winner="bob"
			h=[a+b*2 for a,b in zip(board_a, board_b)]
			history_points.append(ttt.array_to_integer(board_a+board_b))
			history_points_o.append(ttt.array_to_integer(board_b+board_a))
			history_boards.append(h)
		end_of_game=win or tie

	if history:
		print_history(history_boards)
		print_history_points(history_points)
		print_history_points(history_points_o)

	return winner, history_moves

def play_human(act, id_=0, verbose=False): # the human start
	if not win:
		tie=is_tie(board, board2)
	if win:
		you_win=True
	if tie:
		tie=True
	if (not win) and (not tie): 
		win, tie, move=one_move(alice, board2, board)
		print_board_array(board, board2)
		if win:
			i_win=True
		if tie:
			tie=True
	return ttt.array_to_integer(board+board2), i_win, you_win, tie

def input_yes_no(s):
	value=None
	while value is None:
		a=input(s)
		if len(a) > 0:
			if a.lower()[0]=='y':
				value=True
			if a.lower()[0]=='n':
				value=False
		if value is None:
			print("I don't understand, please try again") 
	return value

def play_human_gui(verbose=None, start=None):
	if verbose is None:
		verbose=input_yes_no('do you want some verbosity about what is going on behind the scene ? (y/n)')
	if start is None:
		start=input_yes_no('do you want to start ? (y/n)') 

	print("To play, enter the cellule index like shown here, then enter")
	print("")
	print("%s│%s│%s              %s│%s│%s" % (7,8,9,'e', 'r', 't')) 
	print("─┼─┼─    or you    ─┼─┼─")
	print("%s│%s│%s  can enter   %s│%s│%s" % (4,5,6, 'd', 'f', 'g'))
	print("─┼─┼─    a letter   ┼─┼─")
	print("%s│%s│%s              %s│%s│%s" % (1,2,3, 'c', 'v', 'b'))
	letters='e', 'r', 't', 'd', 'f', 'g', 'c', 'v', 'b' 
	in_progress=True
	board_a=copy.copy(zeros)
	board_b=copy.copy(zeros) 
	alice.verbose=verbose 
	if not start:
		win,tie,move=one_move(alice, board_b, board_a) 
	print("The board is : ")
	print_board_array(board_a, board_b)
	while in_progress:
		available_actions=get_available_actions(list_or(board_a, board_b))
		svailable_actions=','.join([str(a+1) for a in available_actions])
		move=None
		while move is None: 
			smove=input("your turn, what do you do ?")
			if len(smove)>0: 
				if smove in letters:
					imove=letters.index(smove)
				else: 
					imove=int(smove)
					if imove in [7,8,9]:
						imove-=6
					else:
						if imove in [1,2,3]:
							imove+=6
					imove-=1
			if available_actions.count(imove)==0:
				print("I'm afraid that is not possible")
			else:
				move=imove
		old_board=copy.copy(board_a+board_b)
		old_board_b=copy.copy(board_b+board_a)
		board_a[move]=1
		new_board=board_a+board_b
		new_board_b=board_b+board_a
		print("After you play, the board is")
		print_board_array(board_a, board_b)
		#print("%d - %d" % (ttt.array_to_integer(board_a + board_b), ttt.array_to_integer(board_b + board_a)))

		win=False
		tie=False
		win=is_win(board_a)
		if not win:
			tie=is_tie(board_a, board_b)
		if win:
			print("you win")
			in_progress=False
		if tie:
			print("tie")
			in_progress=False 

		if in_progress:
			win, tie, move=one_move(alice, board_b, board_a)
			print("I play in the cell %d" % (move+1))
			print("The board is now") 
			print_board_array(board_a, board_b)
			#print("%d - %d" % (ttt.array_to_integer(board_a + board_b), ttt.array_to_integer(board_b + board_a)))
			if win:
				print("I win")
				in_progress=False
			else:
				if tie:
					print("tie")
					in_progress=False 

def play_all_games(maxcpt=None, verbose=False):
	a=[0,1,2,3,4,5,6,7,8]

	allgames=itertools.permutations(a)
	alice.verbose=verbose
	cpt=0
	a=-1
	totcpt=math.factorial(9)
	for game in allgames: 
		if maxcpt is not None:
			if cpt>maxcpt:
				break

		cpt+=1

		b=int(cpt/totcpt*100)
		if b!=a:
			print("\033[0G%d %%" % b, end="", flush=True)
			a=b
	
		board=copy.copy(zeros)
		board2=copy.copy(zeros) 
		history=[]
		for move in game: 
			available_actions=get_available_actions(list_or(board, board2)) 
			old_board=board+board2
			old_board2=board2+board
			alice.init_status(old_board, available_actions) 
			alice.init_status(old_board2, available_actions) 
			board[move]=1
			new_board=board+board2
			new_board2=board2+board
			h=[a+b*2 for a,b in zip(board, board2)]
			history.append(h)
			alice.learn_path(old_board, move, new_board)
			alice.learn_path_opponent(old_board2, move, new_board2)
			win=is_win(new_board)
			if not win:
				tie=is_tie(board, board2)
			else:
				tie=False

			if (tie) or (win):
				if win:
					alice.learn_points(new_board, 2)
					alice.learn_points(new_board2, -2)
				if tie:
					alice.learn_points(new_board, -1)
					alice.learn_points(new_board2, -1)
				break
			else:
				a=board2
				board2=board
				board=a

		if verbose:
			print_history(history)



			
	print("")

def print_tree(minmax=False):
	if minmax:
		s=alice.print_tree_minmax(0, level_down=99)
	else:
		s=alice.print_tree_maxmin(0, level_down=99)
	pydoc.pager('\n'.join(s))

def print_help():
	print("Commands:")
	print("")
	print("play_human_gui(verbose=False|True, start=False|True")
	print("loop(cpt)")
	print("print_tree(minmax=False|True)")


def init():
	if not alice.try_load():
		alice.verbose=False
		print("Initialization")
		print("playing all games possible")
		play_all_games(verbose=False)
		print("calculate all paths in the tree")
		alice.calculate(0)
		print("saving")
		alice.save()

init()
print_help()
