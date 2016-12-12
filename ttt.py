#!/usr/bin/python3

import importlib

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
		self.leads_to=[]

	def add(self, status):
		if self.leads_to.count(status)==0:
			self.leads_to.append(status)

class AI:
	def __init__(self):
		self.my_status={} # status
		self.op_status={} # status

	def play(self, id_): # i need a list of actions possibles, if i don't know which to pick
# or it can be defined after. i mean i could return none.
		bmove, bpoints=self.calculate(my_status, id_)

		bmove=bmove.choice(bmove)

		
		

	def calculate(self, status_list, id_):
		max_=None
		best=[]
		for i in status_list[id_].leads_to:
			p=status_list[i]
			if max_==None:
				max_=p.points
			if p.points>max_:
				best=[]
				max_=p.points
			best.append(i) # id if the best outcome
		return best, max_

	def learn_path(self, old_status, new_status, opp=False): #old_status and new_status are integers 
		if opp:
			status_list=self.op_status
		else:
			status_list=self.my_status

		if status_list.get(old_status)==None:
			status_list[old_status]=Status()
		status_list[old_status].add(new_status)

	def learn_points(self, status, points, opp=False):
		if opp:
			status_list=self.op_status
		else:
			status_list=self.my_status
		if status_list.get(status)==None:
			status_list[status]=Status()
		status_list[status].points=points 



def play():
	# 

