#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage"""


__ALL__ = [ 'directory' ]

import pygame, math
import enigraph

#def main(bildname):



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

from . import graphics
graphics.init()
Mage = graphics.backend.Mage


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

class LineMages(RamificationMages):
	def relevant_nodes(self):
		return list(self.central_node.children)
	def _sub_line(self, node, offset):
		node.data.goto((offset+self.drawrect.centerx,self.drawrect.centery)) 

class TreeMages(Mages):
	pass
