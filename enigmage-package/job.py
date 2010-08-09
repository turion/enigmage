#! /usr/bin/python
# -*- coding: utf-8 -*-

import multiprocessing
import pygame.time

class Job(object):
	def __init__(self, *args, **kwargs):
		self.dict = {}
		self.dict.update(kwargs)
	def do(self):
		"""Override this with what the job actually does."""
		pass
	
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


class Jobster(multiprocessing.Process):
	"""Job handling class with event loop. It needs pygame to be initialised and currently has no way to check it."""
	def __init__(self, time_per_loop=1000, *args, **kwargs):
		self.extern, self.intern = multiprocessing.Pipe()
		self.pipe_lock = multiprocessing.Lock()
		self.jobs_lock = multiprocessing.Lock()
		self.time_per_loop = time_per_loop
		self.jobs = []
		self.last_time = pygame.time.get_ticks()
		self.usage = 1
		multiprocessing.Process.__init__(self, *args, **kwargs)
	def pickup_job(self, job):
		with self.pipe_lock:
			self.extern.send(job)
	def run(self):
		self.stop = False
		while not self.stop:
			while self.intern.poll():
				job = self.intern.recv()
				self.sort_into_jobs(job)
			self.handle_jobs()
			loop_time_left = self.time_per_loop - self.time_since_last_tick # It's more efficient to calculate self.time_since_last_tick only once
			if loop_time_left >= 0:
				pygame.time.wait(loop_time_left)
			self.usage = float(1 - loop_time_left/self.time_per_loop)
			self.last_time = pygame.time.get_ticks()
	def sort_into_jobs(self, job):
		with self.jobs_lock:
			self.jobs.append(job)
			print self, 'sorted into, has', self.jobs
	def handle_jobs(self):
		with self.jobs_lock:
			print self, 'handles jobs', self.jobs
			while self.jobs and pygame.time.get_ticks() - self.last_time < self.time_per_loop:
				self.handle_job(self.jobs.pop(0))
	def handle_job(self, job):
		print self, ':', job
		job.do()
		if isinstance(job, TermJob):
			print self, 'received job with action', job.dict['action'], ', terminating.'
			self.stop = True
	@property
	def time_since_last_tick(self):
		return pygame.time.get_ticks() - self.last_time

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


class PriorityJobster(Jobster):
	def sort_into_jobs(self, job):
		"""Works by InsertionSort."""
		with self.jobs_lock:
			self.jobs.insert(not_greater_index(self.jobs, job), job)
			print self, 'psorted into, has', self.jobs
