#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage"""


__ALL__ = [ 'directory' ]

import pygame, math
import enigraph

#def main(bildname):

THUMB_SIZE = 200
THUMB_HEIGHT = 150
THUMB_WIDTH = THUMB_SIZE
THUMB_SEPARATOR = 30 # Pixels between two thumbs


def halleluja():
	print("Hallojulia!")

class Var():
	"""Holds various important global variables for the whole enigmage"""
	def __init__(self, screen = None):
		if screen == None:
			size = 800, 600
			self.screen = pygame.display.set_mode(size)
		else: self.screen = screen
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.background.fill((0,0,0))
		self._ticking = 0
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.background.fill((0,0,0))
		self.screen_rect = self.screen.get_rect()
	def tick(self): # Könnte man noch beschleunigen, indem man in der Laufzeit tick umdefiniert/umbindet
		if self._ticking:
			self.time = self.clock.tick(40)
		else:
			self._ticking = 1
			self.clock = pygame.time.Clock()
			self.time = 0
	time = 0
	done = 0

def init(screen):
	global var
	var = Var(screen)
	return True


#def image with thumb
# return image, thumb


def scale_surface_to_size(image, dimensions):
	"""Creates a new surface scaled to width x height. Currently only a wrapper for pygame.transform.scale, but could be replaced for something faster in the future"""
	(width, height) = dimensions
	scaled_image = pygame.transform.scale(image, (width, height))
	return scaled_image

def scale_surface_to_height(image, height):
	"""Creates a new surface with the given height. Height and width are both rounded to an integer value, so float arguments are allowed."""
	width = (height * image.get_width()) / image.get_height()
	return scale_surface_to_size(image, (int(round(width)), int(round(height))))

def scale_surface_to_width(image, width):
	"""Creates a new surface with the given height. Height and width are both rounded to an integer value, so float arguments are allowed."""
	height = (width * image.get_height()) / image.get_width()
	return scale_surface_to_size(image, (int(round(width)), int(round(height))))

def fit_surface_to_size(image, dimensions):
	"""Creates a new surface that fits into a width x height box"""
	(width, height) = dimensions
	if float(image.get_height())*width/(image.get_width()*height) > 1:
		return scale_surface_to_height(image, height)
	else:
		return scale_surface_to_width(image, width)

def fit_surface_to_thumb(image, dimensions=(None, None)):
	"""Creates a thumb from a surface. The height of the thumb is THUMB_HEIGHT. More sophisticated features are likely to be added."""
	(width, height) = dimensions
	return fit_surface_to_size(image, (THUMB_WIDTH, THUMB_HEIGHT))


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
			drawrect = var.screen_rect
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
	



class Mages(pygame.sprite.LayeredUpdates):
	"""Inherits LayeredUpdate. Inherited classes display the mages that are found in the tree rooted at central_node in a specific way."""
	def __init__(self, drawrect, node):
		"""node has to be enigraph.Node and contain enigmage.Mage as data."""
		pygame.sprite.LayeredUpdates.__init__(self) # Die Mage werden von calculate_positions eingewiesen
		self.drawrect = drawrect

		self._focussed_child = 0
		self._central_node = None
		self.central_node = node

		self.add_mages()
		self.calculate_positions() # Sprites zur Gruppe hinzufügen, Positionen berechnen, die in drawrect reinpassen
		self.update_positions() # Sprites an die Positionen verschieben

	def relevant_nodes(self):
		return []
	def add_mages(self):
		#~ temp_group = pygame.sprite.Group(self.sprites())
		self.empty()
		for node in self.relevant_nodes():
			self.add(node.data)
			#~ if not temp_group.has(node.data):
				#~ node.data.beamto(self.drawrect.center)
	def calculate_positions(self):
		"""To be inherited to actually display something."""
		pass
	def update_positions(self):
		"""To be inherited to actually display something."""
		pass
	@property
	def central_node(self):
		return self._central_node # Internally, _central_node is used
	@central_node.setter
	def central_node(self, node):
		if self.central_node:
			self.central_node.data.become_thumb()
		self._central_node = node
		self.central_node.data.become_fullscreen()
		if self.central_node.favourite_child:
			self._focussed_child = self.central_node.children.index(self.central_node.favourite_child)
		else:
			self._focussed_child = 0
		#self.add_mages()
		#self.calculate_positions() # Positionen berechnen, die in drawrect reinpassen
		#self.update_positions() # Sprites an die Positionen verschieben
	def zoom_in(self):
		if self.central_node.children:
			self.central_node = self.central_node.children[self._focussed_child]
			#~ print "Zooming in to ", self.central_node
			self.add_mages()
			self.calculate_positions()
			self.update_positions()
			return True
		else:
			return False
	def zoom_out(self):
		if self.central_node.parent:
			self.central_node.parent.favourite_child = self.central_node
			self.central_node = self.central_node.parent
			#~ print "Zooming out to ", self.central_node
			self.add_mages()
			self.calculate_positions()
			self.update_positions()
		else:
			print("Warning: ", self.central_node, " has no attribute parent!")
	def focus_successor(self):
		if self.central_node.children: # Means that thumbs are floating in front, central_node is background
			if self._focussed_child < len(self.central_node.children)-1:
				self._focussed_child += 1
				self.calculate_positions()
				self.update_positions()
		else: # No thumbs are floating in front, central_node is foreground
			if self.central_node.successor:
				self.zoom_out()
				self.focus_successor() # This is NOT a recursion because when zoomed out, self.central_node will have children
				self.zoom_in()
	def focus_predecessor(self):
		if self.central_node.children:
			if self._focussed_child > 0:
				self._focussed_child -= 1
				self.calculate_positions()
				self.update_positions()
		else:
			if self.central_node.predecessor:
				self.zoom_out()
				self.focus_predecessor() # This is NOT a recursion because when zoomed out, self.central_node will have children
				self.zoom_in()
	# Noch eine Möglichkeit schaffen, dass ein Mage der Gruppe Bescheid sagen kann, wenn es become_fullscreen wird. Die anderen müssen dann so lange weg. Vielleicht bleibt es aber auch dabei, dass man sich einen Mage im Vollbild anschaut, indem man ganz reinzoomt und ihn als Hintergrund behält



class RamificationMages(Mages):
	def relevant_nodes(self):
		return [self.central_node] + list(self.central_node.progeny(generations=2))
	def _main_line(self):
		#main_place_count = (self.drawrect.width - THUMB_WIDTH - 2 * THUMB_SEPARATOR) / (THUMB_WIDTH + THUMB_SEPARATOR) # Might become useful when only drawing the visible	
		if self.central_node.children:
			above = self.central_node.children[self._focussed_child+1:]
			middle = self.central_node.children[self._focussed_child]
			below = self.central_node.children[:self._focussed_child]
			below.reverse()
			#~ print 'Mainline of ', self.central_node, ': Above: ', [str(node) for node in above], ' Middle: ', middle, ' Below: ', [str(node) for node in below]
			self._sub_line(middle, 0)
			for node_index, node in enumerate(above): # enumerate(above) + enumerate(-1, below)
				self._sub_line(node, (1+node_index) * (THUMB_WIDTH + THUMB_SEPARATOR))
			for node_index, node in enumerate(below):
				self._sub_line(node, -(1+node_index) * (THUMB_WIDTH + THUMB_SEPARATOR))
	update_positions = _main_line
	def _sub_line(self, node, offset):
		#sub_place_count = (self.drawrect.width - THUMB_WIDTH - 2 * THUMB_SEPARATOR) / (THUMB_WIDTH + THUMB_SEPARATOR) # Might become useful when only drawing the visible
		# Favourite child in die Mitte, ansonsten Mitte nach oben
		if node.favourite_child:
			self.remove(node.data)
			middle_index = node.children.index(node.favourite_child)
			above = node.children[middle_index+1:]
			middle = node.favourite_child
			below = node.children[:middle_index]
			below.reverse()
		else:
			middle = node
			above = node.children
			below = []
		#~ print "Subline at ", offset, " of ", node, ': Above: ', [str(node) for node in above], ' Middle: ', middle, ' Below: ', [str(node) for node in below]
		if middle:
			middle.data.goto((offset+self.drawrect.centerx,self.drawrect.centery)) 
			for node_index, node in enumerate(above):
				node.data.goto((offset+self.drawrect.centerx, self.drawrect.centery - (1+node_index) * (THUMB_HEIGHT + THUMB_SEPARATOR)))
			for node_index, node in enumerate(below):
				node.data.goto((offset+self.drawrect.centerx, self.drawrect.centery + (1+node_index) * (THUMB_HEIGHT + THUMB_SEPARATOR)))

class TreeMages(Mages):
	pass