#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage.directory
Provides a subclass of a directory node that returns all images in a directory"""

import os, pygame, enigmage, enigtree, enigtree.directory

debug_index = 0

class MageDirNode(enigtree.directory.DirNode):
	#~ def __init__(self, path, *args, **kwargs):
		#~ enigtree.directory.DirNode.__init__(self, path, *args, **kwargs)
	def init_data(self, *args, **kwargs):
		global debug_index
		debug_index = debug_index + 1
		print "Loading ", self.path
		if self.isfile:
			image = pygame.image.load(self.path).convert()
			print "File"
		else:
			image = pygame.image.load('/usr/share/icons/oxygen/48x48/places/folder.png').convert()
			print "Folder"
		mage = enigmage.Mage(image, title=self.path)
		if debug_index > 50: raise Exception
		return mage
	def child_accepted(self, child_path):
		full_child_path = os.path.join(self.path, child_path)
		return os.path.isdir(full_child_path) or (os.path.isfile(full_child_path) and child_path[-4:] in ('.JPG', '.jpg', 'jpeg', 'JPEG'))
	#~ def sort_childs(self): # BROKEN
		#~ childs_dirs = [child for child in self.childs if child.isdir].sort()
		#~ childs_files = [child for child in self.childs if child.isfile].sort()
		#~ print self.path, ": cd ", childs_dirs, " cf ", childs_files
