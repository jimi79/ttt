#!/usr/bin/python3

import importlib
import random

def array_to_integer(array):
	return sum([array[i]*(2**i) for i in range(len(array))])

def integer_to_array(integer):
	a=[int(x) for x in bin(integer)[2:]]	
	a.reverse()
	while len(a)<18:
		a.append(0)
	return a 

class Status:
	def __init__(self):
		self.points=0 # default Value
		self.lt=[]
		self.lto=[] # leads to
		self.htri=[] # How To Rich It : action that has to be taken to go to that new status
		self.htrio=[] # How To Rich It : action that has to be taken to go to that new status
		self.how_to_reach_it=[] # action that has to be taken to go to that new status
		self.name=None
		self.verbose=False
		self.filename=None # no idea how i will store these two arrays of objects
		self.logfilename=None
		self.win=1000

	def add(self, action, status, op):
		if op:
			l=self.lto
			h=self.htrio
		else:
			l=self.lt
			h=self.htri
		if self.l.get(status) is None:
			l.append(status)
			h.append(action) 

class AI:
	def __init__(self):
	# i learn that before leads to after
		self.statuses={} # status

	def play(self, input_): 
		id_=array_to_integer(input_)


		# first we get the max of what we can do
		win=[]
		loss=[] 
		oc=[] # list of outcomes possible, with my points, and opponent's points. Most important is to reach the lowest point for the opponent. and if two matches, we need the highest for me
		for s,a in zip(self.lt, self.htri): # status, action
			if i.points=1000:
				win.append




		bmove, bpoints=self.calculate(id_) 
		if len(bmove)>0:
			bmove=random.choice(bmove) 
		else:
			bmove=None
		return bmove

	def calculate(self, id_):
		max_=None
		best_status=[]
		best_action=[]
		if self.statuses.get(id_)==None:
			self.statuses[id_]=Status()
		for i, j in zip(self.statuses[id_].leads_to, self.statuses[id_].how_to_reach_it):
			p=self.statuses.get(i)
			if not (p is None):
				if max_==None:
					max_=p.points
				if p.points>max_:
					best_status=[]
					best_action=[]
					max_=p.points
				best_status.append(i) # id if the best outcome 
				best_action.append(j)
		if max_!=None:
			self.statuses[id_].points=max_*0.8 # 0.8 parameterable
		return best_action, max_

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

