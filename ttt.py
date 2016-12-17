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
		self.lt=[]
		self.lto=[]
		self.htri=[] # How To Rich It : action that has to be taken to go to that new status
		self.htrio=[] # How To Rich It : action that has to be taken to go to that new status
# true or false ? i think true
		self.minmax=0 # means i took the max of the next one, the min of the next one (unless i reached 1000 or course)
		self.maxmin=0

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

	def play_integer(self, id_, possible_actions, verbose):
# we generate a list of maxmin, based on possible outcomes
		acts=[]
		s=self.statuses.get(id_)
		max_=1 # 0 points is not a goal to reach
		if s is not None:
			for a2,id2 in zip(s.htri, s.lt):
				s2=self.statuses.get(id2)
				if s2 is not None: 
					if verbose:
						print("%d leads to %d which is %d points" % (a2,id2,s2.maxmin))
					if s2.maxmin>max_:
						acts=[]
						max_=s2.maxmin
					if s2.maxmin>=max_: # can only be = or < actually
						acts.append(a2) 
				else:
					if verbose:
						print("%d leads to %d which is unkown" % (a2,id2))

# and we remove each item from the possible_actions list 
		for a in acts:
			possible_actions.remove(a) 

		if verbose:
			print("Bests actions are %s" % acts)
		if len(acts)>0:
			best_action=random.choice(acts)
			if verbose:
				print("Picked best action %d" % best_action)
		else:
			best_action=random.choice(possible_actions)
			if verbose:
				print("Picked random action %d" % best_action)

		return best_action

	def play(self, input_, possible_actions, verbose=False): 
		id_=array_to_integer(input_) 
		return self.play_integer(id_, possible_actions, verbose)

	def learn_path(self, old_status, action, new_status): #old_status and new_status are integers 
		old_status=array_to_integer(old_status)
		new_status=array_to_integer(new_status)
		if self.statuses.get(old_status)==None:
			self.statuses[old_status]=Status()
		self.statuses[old_status].add(action, new_status)

	def learn_path_opponent(self, old_status, action, new_status): #old_status and new_status are integers 
		old_status=array_to_integer(old_status)
		new_status=array_to_integer(new_status)
		if self.statuses.get(old_status)==None:
			self.statuses[old_status]=Status()
		self.statuses[old_status].add_opponent(action, new_status)


	def learn_points(self, status, points): # doesn't change if it's me or the opponent
		status=array_to_integer(status)
		if self.statuses.get(status)==None:
			self.statuses[status]=Status()
		self.statuses[status].points=points 

	def calculate(self, id_):
		s=self.statuses.get(id_)
		if s is not None:
			l=[]
			for i in self.lt: # i need to take the max of it, so i'll update maxmin
				s=self.statuses.get(i)
				if s is not None:
					l.append(s.minmax)
			s.maxmin=max(l)
			l=[]
			for i in self.lto: # i need to take the max of it, so i'll update maxmin
				s=self.statuses.get(i)
				if s is not None:
					l.append(s.maxmin)
			s.minmax=min(l) 

	def save(self):
		pickle.dump(self.statuses, open('ttt.dat', 'wb'))

	def try_load(self):
		if os.path.exists('ttt.dat'):
			self.statuses=pickle.load(open('ttt.dat', 'rb')) 
			print("loaded")
