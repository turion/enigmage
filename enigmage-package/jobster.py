#! /usr/bin/python
# -*- coding: utf-8 -*-

import enigmage.job
import multiprocessing
import pygame.time

try:
	enigmage.var
except AttributeError:
	raise ImportError("enigmage has to be initialised before this module can be imported!")


class Jobster(multiprocessing.Process):
	"""Job handling class with event loop. It needs pygame to be initialised and currently has no way to check it."""
	def __init__(self, time_per_loop=1000, *args, **kwargs):
		self.jobs_lock = multiprocessing.Lock()
		self.time_per_loop = time_per_loop
		self.jobs = [PriorityJob()]
		self.last_time = pygame.time.get_ticks()
		self.usage = 1
		multiprocessing.Process.__init__(self, *args, **kwargs)
	def pickup_job(self, job):
		with self.jobs_lock:
			print self, 'has:', self.jobs
			self.jobs.append(job)
		print 'Picked up Job', job, 'I have:', self.jobs
	def run(self):
		self.stop = False
		while not self.stop:
			self.handle_jobs()			
			loop_time_left = self.time_per_loop - self.time_since_last_tick # It's more efficient to calculate self.time_since_last_tick only once
			if loop_time_left >= 0:
				pygame.time.wait(loop_time_left)
			self.usage = float(1 - loop_time_left/self.time_per_loop)
			self.last_time = pygame.time.get_ticks()
	def handle_jobs(self):
		with self.jobs_lock:
			while self.jobs and pygame.time.get_ticks() - self.last_time < self.time_per_loop:
				print self, 'starts to handle jobs:', self.jobs
				job = self.jobs[0]
				del self.jobs[0]
				print 'Jobs:', self.jobs
				self.handle_job(job)
				#~ self.handle_job(self.jobs.pop(0))
				
	def handle_job(self, job):
		print self, 'handles job', job
		job.do()
		if isinstance(job, TermJob):
			print self, 'received job with action', job.dict['action'], ', terminating.'
			self.stop = True
	@property
	def time_since_last_tick(self):
		return pygame.time.get_ticks() - self.last_time


class PriorityJobster(Jobster):
	def sort_into_jobs(self, job):
		"""Works by InsertionSort."""
		with self.jobs_lock:
			self.jobs.insert(not_greater_index(self.jobs, job), job)
			print self, 'psorted into, has', self.jobs


