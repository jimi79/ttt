#!/usr/bin/python3

import importlib
import os
import pickle
import random

def array_to_integer(array):
	return sum([array[i]*(2**i) for i in range(len(array))])

def substract(lista, listb):
	return [c for c in lista if listb.count(c)==0] 

def inverse_int(val):
	a=integer_to_array(val)
	b=a[9:18]+a[0:9]
	return array_to_integer(b)

def integer_to_array(integer):
	a=[int(x) for x in bin(integer)[2:]]	
	a.reverse()
	while len(a)<18:
		a.append(0)
	return a 

class Status:
	def __init__(self):
		self.lt={}
		self.lto={}
		self.minmax=None # means i took the max of the next one, the min of the next one (unless i reached 1000 or course)
		self.minmax_action=None # means i took the max of the next one, the min of the next one (unless i reached 1000 or course)
		self.maxmin=None
		self.maxmin_action=None
		self.name=None
		self.verbose=False
		self.filename=None # no idea how i will store these two arrays of objects
		self.logfilename=None

	def add(self, action, status):
		l=self.lt
		h=self.htri
		if l.count(status)==0:
			l.append(status)
			h.append(action) 

	def add_opponent(self, action, status):
		l=self.lto
		h=self.htrio
		if l.count(status)==0:
			l.append(status)
			h.append(action) 

class AI:
	def __init__(self):
	# i learn that before leads to after
		self.statuses={} # status
		self.random=True

	def play_integer(self, id_, possible_actions): 
		play_random=False
		# we check unknown outcomes. If any we just try it
		unknown=[a for a,b in self.statuses[id_].lt.items() if b is None]
		if len(unknown) > 0:
			play_random=True
			action=unknown[0]
			if self.verbose:
				print("I never tried action %d, so i'm gonna try now" % action)
		else: 
			s=self.statuses[id_] 
			if s.maxmin_action is None:
				action=random.choice(possible_actions)
			else:
				action=s.maxmin_action
		return action, play_random

	def play(self, input_, possible_actions): 
		id_=array_to_integer(input_) 
		return self.play_integer(id_, possible_actions)

	def init_status(self, id_, possible_actions):
		id_=array_to_integer(id_)
		s=self.statuses.get(id_)
		if s is None:
			if self.verbose:
				print("init status %d with actions %s" % (id_, possible_actions))
			s=Status()
			self.statuses[id_]=s
			for i in possible_actions:
				s.lt[i]=None
				s.lto[i]=None

	def learn_path(self, old_status, action, new_status): 
		old_status=array_to_integer(old_status)
		new_status=array_to_integer(new_status)
		self.statuses[old_status].lt[action]=new_status
		if self.verbose:
			print("Learning from %d with %d leads to %d" % (old_status, action, new_status))

	def learn_path_opponent(self, old_status, action, new_status): #old_status and new_status are integers 
		old_status=array_to_integer(old_status)
		new_status=array_to_integer(new_status)
		self.statuses[old_status].lto[action]=new_status
		if self.verbose:
			print("Learning for opponent, from %d with %d leads to %d" % (old_status, action, new_status))

	def learn_points(self, status, points): # doesn't change if it's me or the opponent
		status=array_to_integer(status)
		s=self.statuses.get(status)
		if s is None:
			s=Status()
			self.statuses[status]=s
		s.minmax=points
		s.maxmin=points
		s.minmax_action=None 
		s.maxmin_action=None

	def calculate(self, id_, lvl=99):
		if lvl>0:
			default=0 # i consider that the min the other can do is 0
			s=self.statuses.get(id_)
			if s is not None:
				if self.verbose:
					print("Calculate %d" % id_)
				l=[]
				for i in s.lto.items(): # i need to take the max of it, so i'll update maxmin
					act=i[0]
					s2=self.statuses.get(i[1])
					if s2 is not None:
						self.calculate(i[1], lvl-1)
						if s2.maxmin is None:
							l.append((default, act))
						else:
							l.append((s2.maxmin, act))
					else:
						l.append((default, act))
				if len(l)>0:
					l=sorted(l)
					#if self.verbose:
					#	print("minmax list %s" % l)
					s.minmax_action=l[0][1]
					s.minmax=l[0][0] 
				l=[]
				default=2
				for i in s.lt.items(): # i need to take the max of it, so i'll update maxmin
					act=i[0]
					s2=self.statuses.get(i[1])
					if s2 is not None:
						self.calculate(i[1], lvl-1)
						if s2.minmax is None:
							l.append((default, act)) 
						else:
							l.append((s2.minmax, act))
					else:
						l.append((default, act))
				if len(l)>0:
					l=sorted(l, reverse=True)
					#if self.verbose:
					#	print("maxmin list %s" % l)
					s.maxmin_action=l[0][1]
					s.maxmin=l[0][0] 
				l=[]
		
	def save(self):
		pickle.dump(self.statuses, open('ttt.dat', 'wb'))

	def print_tree_minmax(self, id_, action=-1, shift='', level_down=4): 
		if len(shift)>60:
			raise Exception("infinite loop")
		if id_ is None:
			print("%s\\ %d->??" % (shift, action))
		else:
			s=self.statuses.get(id_)
			if s is not None:
				print("%s\ %d->%d (min=%s, action=%s)" % (shift, action, id_, s.minmax, s.minmax_action))	
				level_down-=1
				if level_down==0:
					print("%s    \\..." % shift)
				else:
					for i in sorted(s.lto.items(), reverse=True):
						self.print_tree_maxmin(i[1], i[0], shift+'    ', level_down)

	def print_tree_maxmin(self, id_, action=-1, shift='', level_down=4): 
		if len(shift)>60:
			raise Exception("infinite loop")
		if id_ is None:
			print("%s\ %d->??" % (shift, action))
		else:
			s=self.statuses.get(id_)
			if s is not None:
				print("%s\ %d->%d (max=%s, action=%s)" % (shift, action, id_, s.maxmin, s.maxmin_action))
				level_down-=1
				if level_down==0:
					print("%s    \\..." % shift)
				else:
					for i in sorted(s.lt.items()):
						self.print_tree_minmax(i[1], i[0], shift+'    ', level_down) 


	def try_load(self):
		if os.path.exists('ttt.dat'):
			self.statuses=pickle.load(open('ttt.dat', 'rb')) 
			return True
		else:
			return False
