#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage"""


__ALL__ = [ 'directory', 'job', 'loader', 'jobster' ]

import sys, pygame, math
import enigtree

#def main(bildname):

THUMB_SIZE = 200
THUMB_HEIGHT = 150
THUMB_WIDTH = THUMB_SIZE
THUMB_SEPARATOR = 30 # Pixels between two thumbs


def halleluja():
	print "Hallojulia!"

class enigmageError(Exception):
	pass

class eInitError(enigmageError):
	pass

class Var():
	"""Holds various important global variables for the whole enigmage"""
	def __init__(self, screen = None, max_fps=40):
		if screen == None:
			size = 800, 600
			self.screen = pygame.display.set_mode(size)
		else: self.screen = screen
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.background.fill((0,0,0))
		self._ticking = 0
		self.max_fps = max_fps
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.background.fill((0,0,0))
	def tick(self): # Könnte man noch beschleunigen, indem man in der Laufzeit tick umdefiniert/umbindet
		if self._ticking:
			self.time = self.clock.tick(self.max_fps)
		else:
			self._ticking = 1
			self.clock = pygame.time.Clock()
			self.time = 0
	time = 0
	done = 0

def init(size, go_fullscreen=False):
	global var
	if go_fullscreen:
		screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
	else:
		screen = pygame.display.set_mode(size)
	var = Var(screen)
		
	import threading
	global stop_services_lock, stop_services, loop_lock
	stop_services_lock = threading.Lock()
	stop_services = []
	loop_lock = threading.Lock()
	return True

def exit():
	for service_stopper in stop_services:
		service_stopper()
	sys.exit()

def perfect_fit(width1, height1, width2, height2):
	return ( (width1 <= width2) and (height1 == height2) ) or ( (width1 == width2) and (height1 <= height2) )

def scale_surface_to_size(image, (width, height)):
	"""Creates a new surface scaled to width x height. Currently only a wrapper for pygame.transform.scale, but could be replaced for something faster in the future"""
	if (image.get_width(), image.get_height()) == (width, height): # Do not resize if the size is alread correct
		return image
	else:
		print "I have to resize something to", width, height
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

def fit_surface_to_size(image, (width, height)):
	"""Creates a new surface that fits into a width x height box"""
	if float(image.get_height())*width/(image.get_width()*height) > 1:
		return scale_surface_to_height(image, height)
	else:
		return scale_surface_to_width(image, width)

def fit_surface_to_thumb(image, (width, height) = (None, None)):
	"""Creates a thumb from a surface. The height of the thumb is THUMB_HEIGHT. More sophisticated features are likely to be added."""
	#if height == None: height = THUMB_HEIGHT
	#if width == None: return scale_surface_to_height(image, height)
	#else return scale_surface_to_size(image, (width, height))
	return fit_surface_to_size(image, (THUMB_WIDTH, THUMB_HEIGHT))


class Mage(pygame.sprite.Sprite):
	"""enigmage Image handler"""
	_move = 0.0+0.0j
	_velocity = 0.0+0.0j
	_target = 0.0+0.0j
	def __str__(self):
		#str = pygame.sprite.Sprite.__str__(self)
		#if self.title: str += ' "' + self.title + '"'
		#return str
		return str(self.title)
	def __init__(self, raw_image, raw_thumb=None, raw_fullscreen=None, show_as_fullscreen=False, title=None, drawrect=None):
		"""raw_image contains all image information. For performance enhancement it is possible to give thumb and fullscreen images as arguments."""
		pygame.sprite.Sprite.__init__(self)
		
		self.title = title
		
		self._raw_image = raw_image

		self._show_as_fullscreen = show_as_fullscreen
		
		self.drawrect = drawrect # Also None is ok
		
		self.rect = pygame.Rect(0,0,0,0)

		if raw_thumb == None:
			raw_thumb = raw_image
		self.thumb = raw_thumb
		

		if raw_fullscreen == None:
			raw_fullscreen = raw_image
		self.fullscreen = raw_fullscreen
		
		if show_as_fullscreen:
			self.become_fullscreen()
		else: # Supposed to be shown as a thumb
			self.become_thumb()
	@property
	def image(self):
		return self._image
	@image.setter
	def image(self, image):
		"""Has to be set before the mage can be shown or the rect of it accessed. Might somehow include a clipping rect in the future."""
		center = self.rect.center
		self._image, self.rect.size = image, image.get_rect().size
		self.rect.center = center
	@property
	def drawrect(self):
		try:
			return self._drawrect
		except AttributeError:
			return None
	@drawrect.setter
	def drawrect(self, drawrect):
		if not self.drawrect and drawrect:
			self.rect.center = drawrect.center
			self._movetarget(drawrect.center)
		self._drawrect = drawrect
		try:
			self.fullscreen = self.fullscreen  # UGLY
		except AttributeError:
			pass
	@property
	def thumb(self):
		return self._thumb
	@thumb.setter
	def thumb(self, thumb):
		thumb = fit_surface_to_thumb(thumb) # Does not resize if the size is already correct
		self._thumb = thumb
		if not self._show_as_fullscreen:
			self.image = self.thumb # UGLY
	@property
	def fullscreen(self):
		return self._fullscreen
	@fullscreen.setter
	def fullscreen(self, fullscreen):
		if self.drawrect:
			fullscreen = fit_surface_to_size(fullscreen, (self.drawrect.width, self.drawrect.height))  # Does not resize if the size is alread correct
		self._fullscreen = fullscreen
		if self._show_as_fullscreen:
			self.image = self.fullscreen # UGLY
	def _movetarget(self, (target_x, target_y)):
		self._target = target_x + target_y * 1.0j
	def _update_rect_to_target(self):
		if not self._show_as_fullscreen:
			self.rect.center = int(round(self._target.real)), int(round(self._target.imag))
	def beamto(self, (target_x, target_y)):
		#print self, " is beaming to (", target_x, ",", target_y, ")"
		"""Moves _target and subsequently the rect. Accepts float arguments"""
		try:
			self._movetarget((target_x, target_y))
			self._update_rect_to_target()
		except TypeError:
			print "Bad Parameters for Mage.beamto((target_x,target_y))"
	def goto(self, (target_x, target_y)):
		#print self, " is going to (", target_x, ", ", target_y, ")"
		try:
			self._movetarget((target_x, target_y))
		except TypeError:
			print "Bad Parameters for Mage.goto((target_x,target_y))"
	def _attraction(self, time):
		strength = 0.00003

		distance = self._target - (self.rect.centerx + 
		self.rect.centery * 1.0j)
		self._velocity += time * strength * distance
	def _friction(self, time):
		overall_friction = 0.003
		air_friction = 4
		quadratic_air_friction = 1
		self._velocity -= time * overall_friction * self._velocity * (air_friction + quadratic_air_friction * abs(self._velocity)/time)
	def update(self):
		debugstring = str(self)
		debugstring += ' bei ' + str(self.rect.center)
		debugstring += ' v=' + str(self._velocity)
		loop_time = var.time
		while loop_time:
			calc_time = 1
			if loop_time > calc_time:
				time = calc_time
				loop_time = loop_time - calc_time
			else:
				time = loop_time
				loop_time = 0
			self._attraction(time)
			debugstring += ' v+adt=' + str(self._velocity)

			self._friction(time)
			debugstring += ' v+fdt=' + str(self._velocity) + ' dt=' + str(time)
			self._move += self._velocity*time
		if not self._show_as_fullscreen:
			self.rect = self.rect.move(int(round(self._move.real)),int(round(self._move.imag)))
			self._move -= int(round(self._move.real)) + int(round(self._move.imag))*1j # Subtract all the way the rect was really moved
			#if not self.drawrect.colliderect(self.rect): print '"MAMA! Bin weg!" - Dieser Hilferuf kam von ', self, '. Er befindet sich gerade bei ', self.rect.center, '.'
	def become_thumb(self):
		#~ if self._show_as_fullscreen:
			self._show_as_fullscreen = False
			self.image = self.thumb
			self._update_rect_to_target()
			#~ print "Thumb"
	def become_fullscreen(self):
		#~ if not self._show_as_fullscreen:
			self._show_as_fullscreen = True
			self.image = self.fullscreen
			if self.drawrect:
				self.rect.center = self.drawrect.center
		# Der Gruppe bescheid sagen!
	def toggle_fullscreen(self):
		if self._show_as_fullscreen:
			self.become_thumb()
		else:
			self.become_fullscreen()
	def dance(self):
		"""Debug, for identifying"""
		self.rect.center = (self.rect.centerx, self.rect.centery - 30)
		self._goingto = True



class Mages(pygame.sprite.LayeredUpdates):
	"""Inherits LayeredUpdate. Inherited classes display the mages that are found in the tree rooted at central_node in a specific way."""
	def __init__(self, node, drawrect=None, visible = True):
		"""node has to be enigtree.Node and contain enigmage.Mage as data."""
		pygame.sprite.LayeredUpdates.__init__(self) # Die Mage werden von calculate_positions eingewiesen
		if drawrect == None:
			try:
				drawrect = var.screen.get_rect()
			except NameError:
				raise eInitError("enigmage.init has to be called before creating instances of Mages!")
		self.drawrect = drawrect

		self._focussed_child = 0
		self._central_node = None
		self.central_node = node
		self.visible = visible

		self.add_mages()
		self.calculate_positions() # Sprites zur Gruppe hinzufügen, Positionen berechnen, die in drawrect reinpassen
		self.update_positions() # Sprites an die Positionen verschieben

	def relevant_nodes(self):
		return []
	def add_mages(self):
		self.empty()
		relevant_nodes = self.relevant_nodes()
		for node in relevant_nodes:
			self.add(node.data)
			if self.visible:
				node.data.drawrect = self.drawrect
	def calculate_positions(self):
		"""To be inherited to actually display something."""
		pass
	def update_positions(self):
		"""To be inherited to actually display something."""
		pass
	@property
	def central_node(self):
		return self._central_node
	@central_node.setter
	def central_node(self, node):
		if self.central_node:
			self.central_node.data.become_thumb()
		self._central_node = node
		self.central_node.data.become_fullscreen()
		if self.central_node.favourite_child:
			self._focussed_child = self.central_node.childs.index(self.central_node.favourite_child)
		else:
			self._focussed_child = 0
		#self.add_mages()
		#self.calculate_positions() # Positionen berechnen, die in drawrect reinpassen
		#self.update_positions() # Sprites an die Positionen verschieben
	def zoom_in(self):
		if self.central_node.childs:
			self.central_node = self.central_node.childs[self._focussed_child]
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
			print "Warning: ", self.central_node, " has no attribute parent!"
	def focus_successor(self):
		if self.central_node.childs: # Means that thumbs are floating in front, central_node is background
			if self._focussed_child < len(self.central_node.childs)-1:
				self._focussed_child += 1
				self.calculate_positions()
				self.update_positions()
		else: # No thumbs are floating in front, central_node is foreground
			if self.central_node.successor:
				self.zoom_out()
				self.focus_successor() # This is NOT a recursion because when zoomed out, self.central_node will have childs
				self.zoom_in()
	def focus_predecessor(self):
		if self.central_node.childs:
			if self._focussed_child > 0:
				self._focussed_child -= 1
				self.calculate_positions()
				self.update_positions()
		else:
			if self.central_node.predecessor:
				self.zoom_out()
				self.focus_predecessor() # This is NOT a recursion because when zoomed out, self.central_node will have childs
				self.zoom_in()
	def dance(self):
		self.central_node.childs[self._focussed_child].data.dance()

	# Noch eine Möglichkeit schaffen, dass ein Mage der Gruppe Bescheid sagen kann, wenn es become_fullscreen wird. Die anderen müssen dann so lange weg. Vielleicht bleibt es aber auch dabei, dass man sich einen Mage im Vollbild anschaut, indem man ganz reinzoomt und ihn als Hintergrund behält



class RamificationMages(Mages):
	def relevant_nodes(self):
		return [self.central_node] + self.central_node.progeny(2)
	def _main_line(self):
		#main_place_count = (self.drawrect.width - THUMB_WIDTH - 2 * THUMB_SEPARATOR) / (THUMB_WIDTH + THUMB_SEPARATOR) # Might become useful when only drawing the visible	
		if self.central_node.childs:
			above = self.central_node.childs[self._focussed_child+1:]
			middle = self.central_node.childs[self._focussed_child]
			below = self.central_node.childs[:self._focussed_child]
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
			middle_index = node.childs.index(node.favourite_child)
			above = node.childs[middle_index+1:]
			middle = node.favourite_child
			below = node.childs[:middle_index]
			below.reverse()
		else:
			middle = node
			above = node.childs
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
