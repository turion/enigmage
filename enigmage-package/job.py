#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame.time

class Job(object):
	def __init__(self, *args, **kwargs):
		self.dict = {}
		self.dict.update(kwargs)
		self.done = False
	def do(self):
		"""Override this with what the job actually does."""
		self.done = True
	
class PriorityJob(Job):
	"""A priority of 0 is the standard, default value. Higher priorities correspond to higher numbers. The comparisons < and > are implemented to directly compare the priorities. The operator == does *not* compare priorities but still checks, if the jobs are the same instance."""
	def __init__(self, *args, **kwargs):
		if not 'priority' in kwargs.keys():
			kwargs['priority'] = 0
		Job.__init__(self, *args, **kwargs)
	def __lt__(self, other):
		return self.dict['priority'] < other.dict['priority']
	def __gt__(self, other):
		return self.dict['priority'] > other.dict['priority']

class TermJob(PriorityJob):
	def __init__(self, *args, **kwargs):
		kwargs['action'] = 'term'
		PriorityJob.__init__(self, *args, **kwargs)


def not_greater_index(ordered_list, value, key = lambda x:x):
	"""Compares key(item) for all items in the *ordered* list to value and returns the highest index where kex(item) is still not greater. It uses the > comparing operator and no others. FAILS on non-ordered lists without producing an error. Recursive! In principle, the runtime is log(n)."""
	length = len(ordered_list)
	if length == 0: return 0
	#~ elif length == 1:
		#~ if value > key(ordered_list[0]): return 1
		#~ else: return 0
	else:
		if value > key(ordered_list[length/2]):
			return not_greater_index(ordered_list[1+length/2:], value, key=key) + 1 + length/2
		else:
			return not_greater_index(ordered_list[:length/2], value, key=key)

