#! /usr/bin/python
# -*- coding: utf-8 -*-

THUMB_SIZE = 200
THUMB_HEIGHT = 150
THUMB_WIDTH = THUMB_SIZE
THUMB_SEPARATOR = 30 # Pixels between two thumbs

backend = None

def init(**kwargs):
	from . import pygame
	global backend
	backend = pygame
	backend.init(**kwargs)
# Other backends to follow

def scale_surface_to_height(image, height):
	"""Creates a new surface with the given height. Height and width are both rounded to an integer value, so float arguments are allowed."""
	width = (height * image.get_width()) / image.get_height()
	return backend.scale_surface_to_size(image, (int(round(width)), int(round(height))))

def scale_surface_to_width(image, width):
	"""Creates a new surface with the given height. Height and width are both rounded to an integer value, so float arguments are allowed."""
	height = (width * image.get_height()) / image.get_width()
	return backend.scale_surface_to_size(image, (int(round(width)), int(round(height))))

def fit_surface_to_size(image, dimensions):
	"""Creates a new surface that fits into a width x height box"""
	(width, height) = dimensions
	if float(image.get_height())*width/(image.get_width()*height) > 1:
		return scale_surface_to_height(image, height)
	else:
		return scale_surface_to_width(image, width)

def fit_surface_to_thumb(image, dimensions=(None, None)):
	"""Creates a thumb from a surface. The height of the thumb is THUMB_HEIGHT. More sophisticated features are likely to be added."""
	return fit_surface_to_size(image, (THUMB_WIDTH, THUMB_HEIGHT))

import abc
class Group(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def empty(self):
		pass
	@abc.abstractmethod
	def add(self):
		pass
	@abc.abstractmethod
	def remove(self):
		pass
		
