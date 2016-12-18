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
		self.random=True

	def play_integer(self, id_, possible_actions):
# we generate a list of maxmin, based on possible outcomes
		acts=[]
		s=self.statuses.get(id_)
		#max_=None # 0 points is not a goal to reach
		txt=[]
		if s is not None:
			for a2,id2 in s.lt.items():
				if id2 is not None:
					s2=self.statuses.get(id2)
					if s2 is not None: 
						if self.verbose:
							txt.append("%d+%d=%d(%0.2f)" % (id_,a2,id2,s2.minmax))
						#if max_ is None:
						#	max_=s2.minmax
						#if s2.minmax>max_:
						#	acts=[]
						#	max_=s2.minmax
						#if s2.minmax>=max_: # can only be = or < actually
						acts.append((s2.maxmin,a2)) 
					else:
						if self.verbose:
							txt.append("%d+%d=%d(?)" % (id_,a2,id2))
				else:
					if self.verbose:
						txt.append("%d+%d=(?)" % (id_,a2))

		if self.verbose:
			print(",".join(txt))
# and we remove each item from the possible_actions list 
		for a in [b[1] for b in acts]:
			possible_actions.remove(a) 

		for a in possible_actions:
			acts.append((0,a))

		if self.verbose:
			print("actions are : %s" % acts) 
		acts=sorted(acts, reverse=True)
		#acts=sorted(acts)
		if self.verbose:
			print("sorted actions are : %s" % acts) 

		lose_act=[a for a in acts if a[0]==-2] # actions that will make the opponent lose
		win_act=[a for a in acts if a[0]==2] # actions that will make me lose
		positives_act=[a for a in acts if a[0]>0] # positives = the opponents is winning
		negative_act=[a for a in acts if a[0]<0] # positives = the opponents is winning
		nulle_act=[a for a in acts if a[0]==0] # positives = the opponents is winning
		if self.verbose:
			print("win actions are : %s" % win_act) 
			print("positive actions are : %s" % positives_act) 
			print("negative actions are : %s" % negative_act) 
			print("null actions are : %s" % nulle_act) 


		# what list do i pick
		if len(win_act)>0:
			acts2=win_act
		else:
			if len(positives_act)>0:
				acts2=positives_act
			else:
				if len(nulle_act)>0:
					acts2=nulle_act
				else:
					acts2=negative_act

		if self.verbose:
			print("I pick the list %s" % acts2) 

		if self.random:
			best_action=random.choice(acts2)[1] # cruche bordel
		else:
			best_action=acts2[0][1]
		if self.verbose:
			print("Picked best action %d" % best_action)

		return best_action

	def play(self, input_, possible_actions): 
		id_=array_to_integer(input_) 
		return self.play_integer(id_, possible_actions)

	def init_status(self, id_, possible_actions):
		id_=array_to_integer(id_)
		s=self.statuses.get(id_)
		if s is None:
			s=Status()
			self.statuses[id_]=s
			for i in possible_actions:
				s.lt[i]=None
				s.lto[i]=None

	def learn_path(self, old_status, action, new_status): #old_status and new_status are integers 
		old_status=array_to_integer(old_status)
		new_status=array_to_integer(new_status)
		self.statuses[old_status].lt[action]=new_status
		self.calculate(old_status)
		if self.verbose:
			print("Learning from %d with %d leads to %d" % (old_status, action, new_status))

	def learn_path_opponent(self, old_status, action, new_status): #old_status and new_status are integers 
		old_status=array_to_integer(old_status)
		new_status=array_to_integer(new_status)
		self.statuses[old_status].lto[action]=new_status
		self.calculate(old_status)
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

	def calculate(self, id_):
		s=self.statuses.get(id_)
		if s is not None:
			l=[]
			for i in s.lt.keys(): # i need to take the max of it, so i'll update maxmin
				i2=s.lt[i] 
				# we got to invert it to find the next thing ?  
				s2=self.statuses.get(i2)
				if s2 is not None:
					l.append(s2.maxmin)
				else:
					l.append(0)
			if len(l)>0:
				s.minmax=min(l)*0.9
			l=[]
			for i in s.lto.keys(): # i need to take the max of it, so i'll update maxmin
				i2=s.lto[i] 
				s2=self.statuses.get(i2)
				if s2 is not None:
					l.append(s2.minmax)
				else:
					l.append(0)
			if len(l)>0:
				s.maxmin=max(l)*0.9 # doesn't change much, but with that i can now tell the numnber of steps b4 the actual win

	def save(self):
		pickle.dump(self.statuses, open('ttt.dat', 'wb'))

	def print_tree_minmax(self, id_, action=-1, shift='', level_down=4): 
		if level_down==0:
			print("%s\..." % shift)
		else:
			if len(shift)>60:
				raise Exception("infinite loop")
			if id_ is None:
				print("%s\ %d->??" % (shift, action))
			else:
				s=self.statuses.get(id_)
				if s is not None:
					val=s.maxmin
					print("%s\ %d->%d (max=%0.2f)" % (shift, action, id_, val))	
					for i in sorted(s.lto.items(), reverse=True):
						self.print_tree_maxmin(i[1], i[0], shift+'    ', level_down-1)

	def print_tree_maxmin(self, id_, action=-1, shift='', level_down=4): 
		if level_down==0:
			print("%s\..." % shift)
		else:
			if len(shift)>60:
				raise Exception("infinite loop")
			if id_ is None:
				print("%s\ %d->??" % (shift, action))
			else:
				s=self.statuses.get(id_)
				if s is not None:
					val=s.minmax
					print("%s\ %d->%d (min=%0.2f)" % (shift, action, id_, val))
					for i in sorted(s.lt.items()):
						self.print_tree_minmax(i[1], i[0], shift+'    ', level_down-1)




	def try_load(self):
		if os.path.exists('ttt.dat'):
			self.statuses=pickle.load(open('ttt.dat', 'rb')) 
			return True
		else:
			return False
