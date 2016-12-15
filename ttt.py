#!/usr/bin/python3

import importlib
import random

def array_to_integer(array):
	return sum([array[i]*(2**i) for i in range(len(array))])

def substract(lista, listb):
	return [c for c in lista if listb.count(c)==0] 

def integer_to_array(integer):
	a=[int(x) for x in bin(integer)[2:]]	
	a.reverse()
	while len(a)<18:
		a.append(0)
	return a 

class Status:
	def __init__(self):
		self.points=0 # my points
		self.pointso=0 # opponent's points
		self.lt=[]
		self.lto=[] # leads to
		self.htri=[] # How To Rich It : action that has to be taken to go to that new status
		self.htrio=[] # How To Rich It : action that has to be taken to go to that new status
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

	def addo(self, action, status):
		l=self.lto
		h=self.htrio
		if l.count(status)==0:
			l.append(status)
			h.append(action) 

class AI:
	def __init__(self):
	# i learn that before leads to after
		self.statuses={} # status

	def play(self, input_, possible_actions, verbose=False): 
		id_=array_to_integer(input_) 

		# first we get the max of what we can do
		win=[]
		loss=[] 
		good_actions=[]
		bad_actions=[]
		unknown_actions=possible_actions

		self.calculate(id_) # we just update the id_status 
		status=self.statuses.get(id_)
		if not (status is None): 
			for id2,act2 in zip(status.lt, status.htri): # status, action 
				self.calculate(id2) # we just update the id_status 
				status2=self.statuses.get(id2) # status leads to status2 
				if status2.points==1000:
					win.append(act2)
					if unknown_actions.count(act2):
						unknown_actions.remove(act2)
				else:
					for id3,act3 in zip(status2.lto, status2.htrio): 
						status3=self.statuses.get(id2) # status leads to status2 
						if status3.pointso==1000:
							loss.append(act3)
							if unknown_actions.count(act3):
								unknown_actions.remove(act3)
						else:
							if status3.pointso>0:
								bad_actions.append((status3.points, act3)) # we'll sort it afterwards 
							else:
								good_actions.append((status2.points, act3)) # we'll sort it afterwards
							if unknown_actions.count(act3):
								unknown_actions.remove(act3)


		bad_actions=sorted(bad_actions) # last item is the best
		good_actions=sorted(good_actions) # last item is the best

		if len(win)!=0:
			best_action=random.choice(win)
		if len(good_actions)!=0:
			best_action=random.choice(good_actions)
			best_action=best_action[1]
		if len(unknown_actions)!=0:
			best_action=random.choice(unknown_actions)
		if len(bad_actions)!=0:
			best_action=random.choice(bad_actions)
			best_action=best_action[1] 


		return best_action

	def learn_path(self, old_status, action, new_status): #old_status and new_status are integers 
		old_status=array_to_integer(old_status)
		new_status=array_to_integer(new_status)
		if self.statuses.get(old_status)==None:
			self.statuses[old_status]=Status()
		self.statuses[old_status].add(action, new_status)

	def learn_patho(self, old_status, action, new_status): #old_status and new_status are integers 
		old_status=array_to_integer(old_status)
		new_status=array_to_integer(new_status)
		if self.statuses.get(old_status)==None:
			self.statuses[old_status]=Status()
		self.statuses[old_status].addo(action, new_status)

	def learn_points(self, status, points):
		status=array_to_integer(status)
		if self.statuses.get(status)==None:
			self.statuses[status]=Status()
		self.statuses[status].points=points 

	def learn_pointso(self, status, points):
		status=array_to_integer(status)
		if self.statuses.get(status)==None:
			self.statuses[status]=Status()
		self.statuses[status].pointso=points 

	def calculate(self, id_):
		a=self.statuses.get(id_)
		if a is None:
			a=Status()
			self.statuses[id_]=a
		p=[] 
		for i in a.lt:
			s=self.statuses.get(id_)
			if s!=None:
				p.append(s.points)
		if len(p)>0:
			self.points=0.8*max(p)
		p=[]
		for i in a.lto:
			s=self.statuses.get(id_)
			if s!=None:
				p.append(s.pointso)
		if len(p)>0:
			self.points=0.8*max(p) 
