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
		self.points=0 # my points
		self.lt=[]
		self.htri=[] # How To Rich It : action that has to be taken to go to that new status
		self.how_to_reach_it=[] # action that has to be taken to go to that new status
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

class AI:
	def __init__(self):
	# i learn that before leads to after
		self.statuses={} # status

	def play_integer(self, id_, possible_actions, verbose):
		# first we get the max of what we can do
		win=[]
		known_actions=[]
		unknown_actions=possible_actions

		self.calculate(id_) # we just update the id_status 
		status=self.statuses.get(id_)
		if not (status is None): 
			for id2,act2 in zip(status.lt, status.htri): # status, action 
				self.calculate(id2) # we just update the id_status 
				status2=self.statuses.get(id2) # status leads to status2 
				if status2.points==1000:
					if verbose:
						print("%d -%d> %d (win)" % (id_, act2, id2))
					win.append(act2)
					if unknown_actions.count(act2):
						unknown_actions.remove(act2)
				else:
					id2b=inverse_int(id2) # we check through the eyes of the opponent
					self.calculate(id2b) # we just update the id_status 
					status2b=self.statuses.get(id2b)
					if not status2b is None: 
						if verbose:
							print("%d -%d> %d -> %d (me %f, opp %f)" % (id_, act2, id2, id2b, status2.points, status2b.points))
					known_actions.append((status2b.points, status2.points, act2))
					if unknown_actions.count(act2):
						unknown_actions.remove(act2)


		if len(win)!=0:
			best_action=random.choice(win)
		else: 
			known_actions=sorted(known_actions, reverse=True) # last item is the best 

	# not good, i play always the same thing by picking the first
# i should reduce known_actions to get only its best.
			if verbose:
				print("reducing known_actions to its best outcomes")
				print(known_actions)
			if len(known_actions)>0:
				best_opp=known_actions[0][0]
				best_me=known_actions[0][1]
				known_actions=[i for i in known_actions if i[0]==known_actions[0][0] and i[1]==known_actions[0][1]] 
				if verbose:
					print(known_actions)

				best_action=random.choice(known_actions)
				if best_action[0]<=0 and len(unknown_actions)!=0: # if the action we picked, that is the best, is still bad, then we check if there is an unknown action to try out
					best_action=random.choice(unknown_actions)
				else:
					best_action=best_action[2]
			else:
				if len(unknown_actions) > 0:
					best_action=random.choice(unknown_actions)

		if verbose:
			print(win)
			print(known_actions)
			print(unknown_actions)
			print("I play %d" % best_action)

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

	def learn_points(self, status, points):
		status=array_to_integer(status)
		if self.statuses.get(status)==None:
			self.statuses[status]=Status()
		self.statuses[status].points=points 

	def calculate(self, id_):
		a=self.statuses.get(id_)
		if a is None:
			a=Status()
			self.statuses[id_]=a
		p=[] 
		for i in a.lt:
			s=self.statuses.get(i)
			if s!=None:
				p.append(s.points)
		if len(p)>0:
			a.points=0.8*max(p)

	def save(self):
		pickle.dump(self.statuses, open('ttt.dat', 'wb'))

	def try_load(self):
		if os.path.exists('ttt.dat'):
			self.statuses=pickle.load(open('ttt.dat', 'rb')) 
			print("loaded")
