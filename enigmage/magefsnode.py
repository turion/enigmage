#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage.magefsnode
Provides a subclass of an fsnode that returns all images in a directory"""

import os
import pygame
import enigmage
import enigraph, enigraph.fsnode

debug_index = 0

class BackportNode(enigraph.BaseNode):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._favourite_child = None
	def not_my_child(self, message):
		print("Warning: Not my child ({})".format(message))
	@property
	def favourite_child(self):
		if (self._favourite_child is None) or (self._favourite_child in self.children):
			return self._favourite_child
		else:
			self.not_my_child(self._favourite_child)
	@favourite_child.setter
	def favourite_child(self, favourite_child):
		if (self._favourite_child is None) or (favourite_child in self.children):
			self._favourite_child = favourite_child
		else:
			self.not_my_child(favourite_child)
	def _get_children(self):
		try:
			children = self._children #TODO: Better subclass CachedChildrenNode
		except AttributeError:
			children = self._children = list(super()._get_children())
		return children
	def neighbour(self, offset):
		siblings = self.parent.children
		return siblings[siblings.index(self)+offset]
	@property
	def successor(self):
		return self.neighbour(+1)
	@property
	def predecessor(self):
		return self.neighbour(-1)

class MageFSNode(BackportNode, enigraph.fsnode.FSNode):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		global debug_index
		debug_index = debug_index + 1 # Warning if too many Mages are being loaded
		#input("Loading {}".format(self.path))
		if self.isfile:
			image = pygame.image.load(self.path).convert()
		else:
			image = pygame.image.load('/usr/share/icons/oxygen/48x48/places/folder.png').convert()
		mage = enigmage.graphics.backend.Mage(image, title=self.path)
		if debug_index > 100:
			#~ raise Exception
			print("Warning: Too many mages loaded!")
		self.data = mage
	def child_accepted(self, child_path): # FIXME
		full_child_path = os.path.join(self.path, child_path)
		return enigtree.directory.DirNode.child_accepted(self, child_path) and ( os.path.isdir(full_child_path) or (os.path.isfile(full_child_path) and child_path[-4:] in ('.JPG', '.jpg', 'jpeg', 'JPEG')) )
	def sort_childs(self): # FIXME
		childs_dirs = [child for child in self._childs if child.isdir]
		childs_files = [child for child in self._childs if child.isfile]
		childs_dirs.sort(key= lambda child:child.path)
		childs_files.sort(key= lambda child:child.path)
		self._childs = childs_dirs + childs_files
