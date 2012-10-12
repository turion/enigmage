#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage"""

__ALL__ = [ 'directory' ]

import pygame, math
import enigraph


class Var():
	"""Holds various important global variables for the whole enigmage"""
	def __init__(self):
		self._ticking = 0
		self.time = 0
		self.done = 0
	def tick(self): # Könnte man noch beschleunigen, indem man in der Laufzeit tick umdefiniert/umbindet
		if self._ticking:
			self.time = self.clock.tick(40)
		else:
			self._ticking = 1
			self.clock = pygame.time.Clock()
			self.time = 0

from . import graphics, interface, layout, physics

def init(**kwargs):
	global var
	var = Var()
	from .settings import return_settings
	global current_settings
	current_settings = return_settings() # TODO: Keine ideale Nomenklatur, da das Modul auch schon so heißt
	graphics.init(fullscreen=current_settings.fullscreen, **kwargs)
	interface.init()
	physics.init()
	return True

DefaultLayout = layout.Ramification
