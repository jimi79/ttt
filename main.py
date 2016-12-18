#!/usr/bin/python3

import copy
import importlib
import numpy
import pdb
import random
import ttt

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
	old_board2=board2+board
	available_actions=get_available_actions(list_or(board, board2))
	player.init_status(board+board2, available_actions) 
	player.init_status(board2+board, available_actions) 
	#print(ttt.array_to_integer(old_board))
	move=player.play(board + board2, available_actions) # those are lists 
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
	player.learn_path(old_board, move, new_board)
	player.learn_path_opponent(old_board2, move, new_board2)
	return win, tie, move

# should i learn it it can loose ? yeah of course

def one_game(history=False, verbose=False): 
	alice.verbose=verbose
	history_moves=[]
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
		if win:
			winner="alice"
		h=[a+b*2 for a,b in zip(board_a, board_b)]
		history_points.append(ttt.array_to_integer(board_a+board_b))
		history_points_o.append(ttt.array_to_integer(board_b+board_a))
		history_moves.append(h)
		if not win and not tie:
			if verbose:
				print_board_array(board_a, board_b)
				print("bob plays")
			win, tie, move=one_move(alice, board_b, board_a)
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

def multiples_games(cpt, history=False, verbose=False, display=1000, reset=None):
	a=0
	print("%d %%" % a, end="", flush=True)
	totalice=0
	totbob=0
	tottie=0
	tot=0
	cdisplay=0
	if reset is not None:
		if display>reset:
			reset=display
	for i in range(cpt): 
		if display is not None:
			if cdisplay==display:
				print("\033[0Galice %.2f bob %.2f tie %.2f cpt %d" % (totalice/tot*100, totbob/tot*100, tottie/tot*100, tot))
				cdisplay=0
			if reset is not None:
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

def play_human_gui(verbose, start):
	# first we ask if they want some verbosity
	if verbose is None:
		verbose=input_yes_no('do you want some verbosity about what is going on behind the scene ? (y/n)')
	if start is None:
		start=input_yes_no('do you want to start ? (y/n)') 

	print("To play, enter the cellule index like shown here, then enter")
	print("")
	print("%s│%s│%s" % (7,8,9)) 
	print("─┼─┼─")
	print("%s│%s│%s" % (4,5,6))
	print("─┼─┼─")
	print("%s│%s│%s" % (1,2,3))

	in_progress=True
	board_a=copy.copy(zeros)
	board_b=copy.copy(zeros) 

	if not start:
		win,tie,move=one_move(alice, board_b, board_a, verbose=verbose)

	print("The board is : ")
	print_board_array(board_a, board_b)
	while in_progress:
		available_actions=get_available_actions(list_or(board_a, board_b))
		svailable_actions=','.join([str(a+1) for a in available_actions])
		move=None
		while move is None: 
			smove=input("your turn, what do you do ? You can do %s. " % svailable_actions)
			if len(smove)>0: 
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
		old_board=board_a+board_b
		old_board_b=board_b+board_a
		board_a[move]=1
		new_board=board_a+board_b
		new_board_b=board_b+board_a
		print("After you play, the board is")
		print_board_array(board_a, board_b)

		win=False
		tie=False
		win=is_win(board_a)
		if not win:
			tie=is_tie(board_a, board_b)
		if win:
			print("you win")
			in_progress=False
		if tie:
			print("you tied")
			in_progress=False 

		alice.init_status(old_board, available_actions) 
		alice.init_status(old_board_b, available_actions) 
		if win:
			alice.learn_points(board_a+board_b, 2)
			alice.learn_points(board_b+board_a, -2)
		if tie:
			alice.learn_points(board_a+board_b, -1)
			alice.learn_points(board_b+board_a, -1)
		alice.learn_path_opponent(old_board_b, move, new_board_b)
		alice.learn_path(old_board, move, new_board) 

		if in_progress:
			win, tie, move=one_move(alice, board_b, board_a)
			print("I play in the cell %d" % (move+1))
			print("The board is now") 
			print_board_array(board_a, board_b)
			if win:
				print("I win")
				in_progress=False
			else:
				if tie:
		#			print("I tie")
					in_progress=False 

	alice.save() # in case i learned somethg

if alice.try_load():
	print("loaded")
