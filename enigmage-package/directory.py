#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Provides a subclass of a directory node that returns all images in a directory"""

import os, pygame, enigmage, enigtree, enigtree.directory

class MageDirNode(enigtree.directory.DirNode):
	def __init__(self, path, *args, **kwargs):
		enigtree.directory.DirNode.__init__(self, path, *args, **kwargs)
	def init_data(self, *args, **kwargs):
		print "Loading ", self.path
		if self._isfile:
			image = pygame.image.load(self.path).convert()
		else:
			image = pygame.image.load('/usr/share/icons/Human/48x48/places/folder.png').convert()
		mage = enigmage.Mage(image, title=self._path)
		return mage
	def child_accepted(self, child):
		full_child_path = os.path.join(self.path, child)
		return os.path.isdir(full_child_path) or (os.path.isfile(full_child_path) and child[-4:] in ('.JPG', '.jpg', 'jpeg', 'JPEG'))
	def sort_childs(self, childs):
		childs_dirs = [child for child in childs if child.isdir]
		childs_files = [child for child in childs if child.isfile]
		print self.path, ": cd ", childs_dirs, " cf ", childs_files
		return childs_dirs.sort() + childs_files.sort()
