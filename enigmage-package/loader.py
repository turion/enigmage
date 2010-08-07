#! /usr/bin/python
# -*- coding: utf-8 -*-

import enigmage.job, enigmage.directory
import enigmage
import Image, pygame, pygame.image

try:
	enigmage.var
except AttributeError:
	raise ImportError("enigmage has to be initialised before this module can be imported!")
	

class MageLoadJob(enigmage.job.PriorityJob):
	def __init__(self, mage, fullscreen_path=None, thumb_path=None, *args, **kwargs):
		kwargs['action'] = 'MageLoad'
		enigmage.job.PriorityJob.__init__(self, *args, **kwargs)
		self.mage = mage
		self.fullscreen_path = fullscreen_path
		#~ if thumb_path == None: thumb_path = fullscreen_path
		self.thumb_path = thumb_path
	def do(self):
			print "I will load a mage now"
			fullscreen, thumb = PIL_to_pygame_fullscreen_and_or_thumb_image(self.fullscreen_path, self.thumb_path)
			if fullscreen:
				self.mage.fullscreen = fullscreen
			if thumb:
				self.mage.thumb = thumb
			# Find a way to refresh .image


def PIL_to_pygame_fullscreen_and_or_thumb_image(fullscreen_path, thumb_path, drawrect=None):
	"""Technical. Maybe this should load something for raw_image too?"""
	PIL_thumb = None
	pygame_fullscreen = None
	pygame_thumb = None
	if drawrect == None:
		drawrect = enigmage.var.screen_rect

	if fullscreen_path:
		fullscreen = Image.open(fullscreen_path)
		if not thumb_path:
			thumb = fullscreen.copy()
		fullscreen.resize((drawrect.width, drawrect.height))
		pygame_fullscreen = pygame.image.fromstring(fullscreen.tostring(), fullscreen.size, fullscreen.mode).convert()

	if thumb_path:
		thumb = Image.open(thumb_path)
	if thumb:
		thumb.thumbnail((enigmage.THUMB_HEIGHT, enigmage.THUMB_WIDTH))
		pygame_thumb = pygame.image.fromstring(thumb.tostring(), thumb.size, thumb.mode)
	return pygame_fullscreen, pygame_thumb



sandglass_fullscreen, sandglass_thumb = PIL_to_pygame_fullscreen_and_or_thumb_image('/usr/share/icons/oxygen/128x128/apps/tux.png', None)

mage_loader = PriorityJobster()
mage_loader.start()

with enigmage.stop_services_lock:
	enigmage.stop_services.append(mage_loader.join)

class LazyMageDirNode(enigmage.directory.MageDirNode):
	"""So far without thumbs on their own."""
	def init_data(self, *args, **kwargs):
		if self.isfile:
			global sandglass_fullscreen, sandglass_thumb
			mage = enigmage.Mage(sandglass_fullscreen, raw_fullscreen=sandglass_fullscreen, raw_thumb=sandglass_thumb) # Ugly: raw_image should be something else
			
			global mage_loader
			job = MageLoadJob(mage, self.path)
			mage_loader.pickup_job(job)
		else:
			image = pygame.image.load('/usr/share/icons/oxygen/48x48/places/folder.png').convert()
			mage = enigmage.Mage(image, title=self.path) # This is ugly!!
		return mage

# TODO: Who starts the MageLoader? Avoid circular dependencies
