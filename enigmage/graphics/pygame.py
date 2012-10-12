#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame

def scale_surface_to_size(image, dimensions):
	"""Creates a new surface scaled to width x height. Currently only a wrapper for pygame.transform.scale, but could be replaced for something faster in the future"""
	return pygame.transform.scale(image, dimensions)

from ..graphics import fit_surface_to_thumb, fit_surface_to_size
from .. import var #TODO Das ist nur für die Physik, die ihre eigene Zeitzählung mitbringen sollte

def init(existing_screen=None, fullscreen=False):
	pygame.init()
	global screen, background
	if existing_screen == None:
		if fullscreen:
			screen_size = 1024, 768
		else:
			screen_size = 800, 600
		screen = pygame.display.set_mode(screen_size, fullscreen and pygame.FULLSCREEN or 0)
	else:
		screen = existing_screen
	background = pygame.Surface(screen.get_size()).convert()
	background.fill((0,0,0))


class Mage(pygame.sprite.Sprite):
	"""enigmage Image handler"""
	_movestep = 10.0
	_velstep = 0.1
	_move = 0.0+0.0j
	_velocity = 0.0+0.0j
	_goingto = False
	_target = 0.0+0.0j
	_drawrect = None
	#_blowing = 0.0
	#_blowheight = 0
	_show_as_fullscreen = False
	_raw_image = None
	_title = ''
	def __str__(self):
		#str = pygame.sprite.Sprite.__str__(self)
		#if self._title: str += ' "' + self._title + '"'
		#return str
		return self._title
	def __init__(self, raw_image, raw_thumb=None, drawrect=None, show_as_fullscreen=False, target_x = None, target_y = None, title=None):
		"""raw_image contains all image information. For future performance enhancement it is possible to give thumb and fullscreen images as arguments."""
		pygame.sprite.Sprite.__init__(self)
		
		if title: self._title = title
		
		if raw_thumb == None:
			raw_thumb = raw_image
		self.thumb = fit_surface_to_thumb(raw_thumb)
		
		self._raw_image = raw_image
		if drawrect == None:
			drawrect = screen.get_rect()
		self.assign_drawrect(drawrect)

		try:
			self._movetarget((target_x, target_y))
		except TypeError: 
			#print "Bad or no parameters target_x, target_y to Mage.__init__(...). Defaulting to the middle of the drawrect (could be the screen)."
			self._movetarget((self._drawrect.centerx,self._drawrect.centery))
		
		self._show_as_fullscreen = show_as_fullscreen
		if self._show_as_fullscreen:
			self.become_fullscreen()
		else: # Supposed to be shown as a thumb
			self.become_thumb()
	def assign_image(self, image, rect=None):
		"""Has to be called before the mage can be shown or the rect of it accessed. Might include a clipping rect in the future."""
		if rect == None: rect = image.get_rect()
		self.image, self.rect = image, rect
		self._update_rect_to_target()
	def assign_drawrect(self, drawrect):
		self._drawrect = drawrect
		self.fullscreen = fit_surface_to_size(self._raw_image, (self._drawrect.width, self._drawrect.height))
	def right(self):
		self._velocity += self._velstep
	def left(self):
		self._velocity -= self._velstep
	def up(self):
		self._velocity -= self._velstep * 1.0j
	def down(self):
		self._velocity += self._velstep * 1.0j
	#def right(self): # 10 Pixel pro Tastendruck
		#self._move += self._movestep
	#def left(self):
		#self._move -= self._movestep
	#def up(self):
		#self._move -= self._movestep * 1.0j
	#def down(self):
		#self._move += self._movestep * 1.0j
	def _movetarget(self, dimensions):
		(target_x, target_y) = dimensions
		self._target = target_x + target_y * 1.0j
	def _update_rect_to_target(self):
		if not self._show_as_fullscreen:
			self.rect.centerx, self.rect.centery = int(round(self._target.real)), int(round(self._target.imag))
	def beamto(self, dimensions):
		#print self, " is beaming to (", target_x, ", ", target_y, ")"
		"""Moves _target and subsequently the rect. Accepts float arguments"""
		(target_x, target_y) = dimensions
		try:
			self._movetarget((target_x, target_y))
			self._update_rect_to_target()
		except TypeError:
			print("Bad Parameters for Mage.beamto((target_x,target_y))")
	def goto(self, dimensions):
		#print self, " is going to (", target_x, ", ", target_y, ")"
		(target_x, target_y) = dimensions
		try:
			self._movetarget((target_x, target_y))
			self._goingto = True
		except TypeError:
			print("Bad Parameters for Mage.goto((target_x,target_y))") # In this case, self._goingto is left untouched
	def _attraction(self):
		strength = 0.00003

		#weak_scale = 10 # Pixels
		#anharmonicity = + 0.000005		
		#bumpsize = 30 # Pixels
		#bumpheight = 0
		
		snap = 2 # Pixels
		distance = self._target - (self.rect.centerx + 
		self.rect.centery * 1.0j)
		#self._velocity += strength * distance * math.atan(abs(distance)/weak_scale) / (0.0001 + abs(distance))
		#print (1 + anharmonicity * (abs(distance)**2))
		#self._velocity += var.time * strength * distance * (1 + anharmonicity * (abs(distance)**2))
		#self._velocity += var.time * strength * distance * (1 + bumpheight / (1 + (abs(distance)/bumpsize)**2))
		self._velocity += var.time * strength * distance
		if abs(distance) < snap:
			self._goingto = False
			#print "Went to"
	def _friction(self):
		overall_friction = 0.003
		ground_friction = 1
		air_friction = 2
		self._velocity -= var.time * overall_friction * self._velocity * (air_friction + ground_friction/(1+abs(self._velocity)))
	def update(self):
		debugstring = str(self) + ' bei ' + str(self.rect.center) + ' v=' + str(self._velocity)
		if not self._show_as_fullscreen: # Doing the physics for the thumb moving
			if self._goingto:
				self._attraction()
				debugstring += ' v+adt=' + str(self._velocity)
			self._friction()
			debugstring += ' v+fdt=' + str(self._velocity) + ' dt=' + str(var.time)
			self._move += self._velocity*var.time
			self.rect = self.rect.move(int(round(self._move.real)),int(round(self._move.imag)))
			self._move -= int(round(self._move.real)) + int(round(self._move.imag))*1j
			#if self._goingto: print debugstring
			#if self._blowing: self._blowstep()
	#def _blowstep(self):
		#"""For a smooth scaling. Costs to much resources in SDL, but likely to be implemented in OpenGL."""
		#blowingspeed = 1.0 / 1000 # First number in seconds
		#self._blowing += var.time * blowingspeed
		#if self._blowing > 1: self._blowing = 1
		#self._setheight(int(self._blowheight*self._blowing))
		#if self._blowing > 1: self._blowing = 0
		
		#if not self._drawrect.colliderect(self.rect): print '"MAMA! Bin weg!" - Dieser Hilferuf kam von ', self, '. Er befindet sich gerade bei ', self.rect.center, '.'
	def _setsize(self, dimensions):
		"""Manually set the shown image to a resized thumb or fullscreen"""
		(width, height) = dimensions
		if self._thumb: show_image = self.thumb
		else: show_image = self.fullscreen
		self.assign_image(fit_surface_to_size(show_image, (width, height)))
	def become_thumb(self):
		self._show_as_fullscreen = False
		self._goingto = True
		self.assign_image(self.thumb)
		self._update_rect_to_target()
	def become_fullscreen(self):
		if not self._show_as_fullscreen:
			self._show_as_fullscreen = True
			self.assign_image(self.fullscreen)
			self._goingto = False
			self.rect.center = self._drawrect.center
		# Der Gruppe bescheid sagen!
	def toggle_fullscreen(self):
		if self._show_as_fullscreen:
			#print "Becoming thumb"
			self.become_thumb()
		else:
			#print "Becoming fullscreen"
			self.become_fullscreen()
