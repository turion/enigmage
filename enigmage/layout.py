#! /usr/bin/python
# -*- coding: utf-8 -*-

from . import graphics

class Layout:
	"""Inherited classes display the mages that are found in the tree rooted at central_node in a specific way."""
	def __init__(self, central_node, drawrect=None):
		"""node has to be enigraph.Node and contain enigmage.Mage as data."""
		self.group = graphics.backend.Group()
		if drawrect == None:
			drawrect = graphics.backend.screen.get_rect()
		self.drawrect = drawrect

		self._focussed_child = 0
		self._central_node = None
		self.central_node = central_node

		self.add_mages()
		self.calculate_positions() # Sprites zur Gruppe hinzufügen, Positionen berechnen, die in drawrect reinpassen
		self.update_positions() # Sprites an die Positionen verschieben

	def relevant_nodes(self):
		return []
	def add_mages(self):
		#~ temp_group = graphics.backend.Group(self.group.sprites())
		self.group.empty()
		for node in self.relevant_nodes():
			self.group.add(node.data)
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



class Ramification(Layout):
	def relevant_nodes(self):
		return [self.central_node] + list(self.central_node.progeny(generations=2))
	def _main_line(self):
		#main_place_count = (self.drawrect.width - graphics.THUMB_WIDTH - 2 * graphics.THUMB_SEPARATOR) / (graphics.THUMB_WIDTH + graphics.THUMB_SEPARATOR) # Might become useful when only drawing the visible	
		if self.central_node.children:
			above = self.central_node.children[self._focussed_child+1:]
			middle = self.central_node.children[self._focussed_child]
			below = self.central_node.children[:self._focussed_child]
			below.reverse()
			#~ print 'Mainline of ', self.central_node, ': Above: ', [str(node) for node in above], ' Middle: ', middle, ' Below: ', [str(node) for node in below]
			self._sub_line(middle, 0)
			for node_index, node in enumerate(above): # enumerate(above) + enumerate(-1, below)
				self._sub_line(node, (1+node_index) * (graphics.THUMB_WIDTH + graphics.THUMB_SEPARATOR))
			for node_index, node in enumerate(below):
				self._sub_line(node, -(1+node_index) * (graphics.THUMB_WIDTH + graphics.THUMB_SEPARATOR))
	update_positions = _main_line
	def _sub_line(self, node, offset):
		#sub_place_count = (self.drawrect.width - graphics.THUMB_WIDTH - 2 * graphics.THUMB_SEPARATOR) / (graphics.THUMB_WIDTH + graphics.THUMB_SEPARATOR) # Might become useful when only drawing the visible
		# Favourite child in die Mitte, ansonsten Mitte nach oben
		if node.favourite_child:
			self.group.remove(node.data)
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
				node.data.goto((offset+self.drawrect.centerx, self.drawrect.centery - (1+node_index) * (graphics.THUMB_HEIGHT + graphics.THUMB_SEPARATOR)))
			for node_index, node in enumerate(below):
				node.data.goto((offset+self.drawrect.centerx, self.drawrect.centery + (1+node_index) * (graphics.THUMB_HEIGHT + graphics.THUMB_SEPARATOR)))

class Line(Ramification):
	def relevant_nodes(self):
		return list(self.central_node.children)
	def _sub_line(self, node, offset):
		node.data.goto((offset+self.drawrect.centerx,self.drawrect.centery)) 

class Tree(Layout):
	pass