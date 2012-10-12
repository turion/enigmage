#! /usr/bin/python
# -*- coding: utf-8 -*-

def init():
	from . import purepython
	global backend
	backend = purepython

class Model: # TODO Die Namen müssen doch nicht mit _ anfangen
	def __init__(self, mage):
		self.mage = mage
		self._goingto = False
		self._velocity = 0.0 + 0.0j
		self._move = 0.0 + 0.0j
	def _attraction(self):
		pass
	def _friction(self):
		pass
	def update(self):
		return (0,0)
