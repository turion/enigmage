#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage.magefsnode
Provides a subclass of an fsnode that returns all images in a directory"""

import os
import pygame
import enigmage
import enigraph, enigraph.fsnode

debug_index = 0

class MageFSNode(enigraph.fsnode.FSNode):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		global debug_index
		debug_index = debug_index + 1 # Warning if too many Mages are being loaded
		#~ print "Loading ", self.path
		if self.isfile:
			image = pygame.image.load(self.path).convert()
		else:
			image = pygame.image.load('/usr/share/icons/oxygen/48x48/places/folder.png').convert()
		mage = enigmage.Mage(image, title=self.path)
		if debug_index > 100:
			#~ raise Exception
			print("Warning: Too many mages loaded!")
		return mage
	def child_accepted(self, child_path): # FIXME
		full_child_path = os.path.join(self.path, child_path)
		return enigtree.directory.DirNode.child_accepted(self, child_path) and ( os.path.isdir(full_child_path) or (os.path.isfile(full_child_path) and child_path[-4:] in ('.JPG', '.jpg', 'jpeg', 'JPEG')) )
	def sort_childs(self): # FIXME
		childs_dirs = [child for child in self._childs if child.isdir]
		childs_files = [child for child in self._childs if child.isfile]
		childs_dirs.sort(key= lambda child:child.path)
		childs_files.sort(key= lambda child:child.path)
		self._childs = childs_dirs + childs_files
