#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage.loader - Lazy image loading"""

import enigmage.job, enigmage.jobster, enigmage.directory
import enigmage
import Image, pygame, pygame.image

if not enigmage.initialised:
	raise enigmage.eInitError("importing enigmage.loader")

class MageLoadJob(enigmage.job.PriorityJob):
	def __init__(self, node, fullscreen_path=None, thumb_path=None, *args, **kwargs):
		self.node = node
		self.fullscreen_path = fullscreen_path
		#~ if thumb_path == None: thumb_path = fullscreen_path
		self.thumb_path = thumb_path
		kwargs['action'] = 'MageLoad'
		enigmage.job.PriorityJob.__init__(self, *args, **kwargs)
	def do(self):
		#~ print "I will load a mage now"
		fullscreen, thumb = PIL_to_pygame_fullscreen_and_or_thumb_image(self.fullscreen_path, self.thumb_path)
		#~ with enigmage.loop_lock:
		if fullscreen:
			self.node.data.fullscreen = fullscreen
		if thumb:
			self.node.data.thumb = thumb
		# Find a way to refresh .image
		enigmage.job.PriorityJob.do(self)


def PIL_to_pygame_fullscreen_and_or_thumb_image(fullscreen_path, thumb_path, drawrect=None): # Liefert die die richtigen Größen? Dauert das Resize zu lang?
	"""Technical. Maybe this should load something for raw_image too?"""
	PIL_thumb = None
	pygame_fullscreen = None
	pygame_thumb = None
	if drawrect == None:
		drawrect = enigmage.screen.get_rect()
	if fullscreen_path:
		fullscreen = Image.open(fullscreen_path)
		if not thumb_path:
			thumb = fullscreen.copy()
		resize_to_width, resize_to_height = enigmage.perfect_fit(fullscreen.size[0], fullscreen.size[1], drawrect.width, drawrect.height)
		#~ print "PIL drawrect", drawrect, "PIL resize fullscreen to ", resize_to_width, resize_to_height
		fullscreen = fullscreen.resize((resize_to_width, resize_to_height))
		#~ fullscreen.thumbnail((drawrect.width, drawrect.height))
		pygame_fullscreen = pygame.image.fromstring(fullscreen.tostring(), fullscreen.size, fullscreen.mode).convert()
		#~ print "PIL fullscreen has size", fullscreen.size, "pygame_fullscreen has size", pygame_fullscreen.get_width(), pygame_fullscreen.get_height()


	if thumb_path:
		thumb = Image.open(thumb_path)
	if thumb:
		#~ thumb.thumbnail((enigmage.THUMB_WIDTH, enigmage.THUMB_HEIGHT))
		resize_to_width, resize_to_height = enigmage.perfect_fit(thumb.size[0], thumb.size[1], enigmage.THUMB_WIDTH, enigmage.THUMB_HEIGHT)
		thumb = thumb.resize((resize_to_width, resize_to_height))
		pygame_thumb = pygame.image.fromstring(thumb.tostring(), thumb.size, thumb.mode).convert()
		#~ print "PIL thumb has size", thumb.size, "pygame_thumb has size", pygame_thumb.get_width(), pygame_thumb.get_height()
	return pygame_fullscreen, pygame_thumb


sandglass_fullscreen, sandglass_thumb = PIL_to_pygame_fullscreen_and_or_thumb_image('/usr/share/icons/oxygen/128x128/apps/tux.png', None)

# Die hier auch vergrößern

#~ folder = pygame.image.load('/usr/share/icons/oxygen/48x48/places/folder.png').convert()
folder_fullscreen, folder_thumb = PIL_to_pygame_fullscreen_and_or_thumb_image('/usr/share/icons/oxygen/48x48/places/folder.png', None)

mage_loader = enigmage.jobster.PriorityJobster()
mage_loader.start()

def shoot_mage_loader():
	mage_loader.pickup_job(enigmage.job.TermJob(priority=3))

with enigmage.stop_services_lock:
	enigmage.stop_services.append(shoot_mage_loader)
	enigmage.stop_services.append(mage_loader.join)


class LazyMageDirNode(enigmage.directory.MageDirNode):
	"""So far without thumbs on their own."""
	def __init__(self, path, *args, **kwargs):
		enigmage.directory.MageDirNode.__init__(self, path, *args, **kwargs)
	def init_data(self, *args, **kwargs):
		if self.isfile:
			global sandglass_fullscreen, sandglass_thumb
			# Schönerweise sollte man das dict anlegen. Aber dafür braucht man die Information über das drawrect vor der Instanzierung des Mage
			#~ print "Doing tux mage"
			mage = enigmage.Mage(sandglass_fullscreen, raw_fullscreen=sandglass_fullscreen, raw_thumb=sandglass_thumb) # Ugly: raw_image should be something else
			#~ print "Did tux mage"
			
			self.job = MageLoadJob(self, fullscreen_path=self.path, thumb_path=self.path)
			
			global mage_loader
			mage_loader.pickup_job(self.job) # For priority stuff later
		else:
			#~ print "Doing folder mage"
			mage = enigmage.Mage(folder_fullscreen, raw_fullscreen=folder_fullscreen, raw_thumb=folder_thumb, title=self.path) # This is ugly!!
			#~ print "Did folder mage"
		return mage

