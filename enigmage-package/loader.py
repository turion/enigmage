#! /usr/bin/python
# -*- coding: utf-8 -*-

import multiprocessing, time

class Job(object):
	def __init__(self, *args, **kwargs):
		self.dict = {}
		self.dict.update(kwargs)
		
class TermJob(Job):
	def __init__(self, *args, **kwargs):
		kwargs['action'] = 'term'
		Job.__init__(self, *args, **kwargs)


class Loader(multiprocessing.Process):
	def __init__(self, idle_per_loop=0.1, *args, **kwargs):
		multiprocessing.Process.__init__(self, *args, **kwargs)
		self.extern, self.intern = multiprocessing.Pipe()
		self.idle_per_loop = idle_per_loop
		self.jobs = []
	def run(self):
		self.stop = False
		while not self.stop:
			while self.intern.poll():
				self.sort_into_jobs(self.intern.recv())
			self.handle_jobs()
			time.sleep(self.idle_per_loop)
	def sort_into_jobs(self, job):
		self.jobs.append(job)
	def handle_jobs(self):
		while self.jobs:
			self.handle_job(self.jobs.pop(0))
	def handle_job(self, job):
		if isinstance(job, TermJob):
			print 'Received job with action', job.dict['action'], ', terminating.'
			self.stop = True
