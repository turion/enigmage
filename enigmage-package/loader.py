#! /usr/bin/python
# -*- coding: utf-8 -*-

import enigmage.job, enigmage.directory, enigmage
import Image

class MageLoadJob(enigmage.job.PriorityJob):
	def __init__(self, mage, fullscreen_path=None, thumb_path=None, *args, **kwargs):
		kwargs['action'] = 'MageLoad'
		Job.__init__(self, *args, **kwargs)
		self.mage = mage
		self.fullscreen_path = fullscreen_path
		#~ if thumb_path == None: thumb_path = fullscreen_path
		self.thumb_path = thumb_path

def PIL_to_pygame_fullscreen_and_or_thumb_image(fullscreen_path, thumb_path):
	"""Technical. Maybe this should load something for raw_image too?"""
	PIL_thumb = None
	pygame_fullscreen = None
	pygame_thumb = None

	if fullscreen_path:
		fullscreen = Image.open(job.fullscreen_path)
		if not thumb_path:
			thumb = fullscreen.copy()
		fullscreen.resize((job.mage.drawrect.width, job.mage.drawrect.height))
		pygame_fullscreen = pygame.image.fromstring(fullscreen.tostring(), image.size).convert()

	if thumb_path:
		thumb = Image.open(job.thumb_path)
	if thumb:
		thumb.thumbnail((enigmage.THUMB_HEIGHT, enigmage.THUMB_WIDTH))
		pygame_thumb = pygame.image.fromstring(thumb.tostring(), thumb.size)
	return pygame_fullscreen, pygame_thumb

class MageLoader(enigmage.job.PriorityJobster):
	def handle_job(self, job):
		enigmage.job.PriorityJobster.handle_job(self, job)
		if isinstance(job, MageLoadJob):
			fullscreen, thumb = PIL_to_pygame_fullscreen_and_or_thumb_image(job.fullscreen_path, job.thumb_path)
			if fullscreen:
				job.mage.fullscreen = fullscreen
			if thumb:
				job.mage.thumb = thumb
				

sandglass_fullscreen, sandglass_thumb = PIL_to_pygame_fullscreen_and_or_thumb_image('/usr/share/icons/oxygen/128x128/apps/tux.png', None)
	
class LazyMageDirNode(enigmage.directory.MageDirNode)
	"""So far without thumbs on their own."""
	def init_data(self, *args, **kwargs):
		global sandglass_fullscreen, sandglass_thumb
		mage = enigmage.Mage(sandglass_fullscreen, raw_fullscreen=sandglass_fullscreen, raw_thumb=sandglass_thumb) # Ugly: raw_image should be something else
		job = MageLoadJob(mage, self.path)

# TODO: Who starts the MageLoader? Avoid circular dependencies
