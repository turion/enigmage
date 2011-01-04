#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage.constants
Import all the constants defined in enigmage without importing enigmage."""

#DO NOT import enigmage here!

THUMB_SIZE = 200
THUMB_HEIGHT = 150
THUMB_WIDTH = THUMB_SIZE
THUMB_SEPARATOR = 30 # Pixels between two thumbs

class EnigmageError(StandardError):
	pass

class EnigmageValueError(EnigmageError, ValueError):
	pass

class InitError(EnigmageError):
	"""This error should be raised whenever something accesses some enigmage functionality that cannot be accessed before initialising enigmage, i.e. runtime objects like the screen."""
	def __init__(self, caller = "doing this"):
		self.caller = caller
	def __str__(self):
		return "enigmage.init has to be called before " + self.caller + "!"
