#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage-Spielwiese
Testing for new enigmage and enigtree components"""

import pygame.image, Image, enigmage
import pygame.time

import enigtree.directory

pygame.display.set_mode((800, 600))

node_big = enigtree.directory.DirNode('/home/turion/Fotos/selection enigmage_big/')
node_sm = enigtree.directory.DirNode('/home/turion/Fotos/selection enigmage/')

paths = [node.path for node in node_big.progeny() + node_sm.progeny() if node.path[-4:] in ['.JPG', '.jpg'] ]

class Clocksum(object):
	def __init__(self):
		self.new()
	def add(self, time):
		self.last_time = time
		self.sum = self.sum + time
		print time
	def new(self):
		self.sum = 0
	def total(self):
		print 'Total:', self.sum
		self.new()
		
clocksum = Clocksum()

clock = pygame.time.Clock()
clock.tick()

print 'Loading pygame raw images'

raw_images = [pygame.image.load(path) for path in paths]

clocksum.add(clock.tick())

print 'Converting pygame raw images'

conv_images = [image.convert() for image in raw_images]

clocksum.add(clock.tick())

print 'Resizing pygame to fullscreens'

pyfull_images = [enigmage.scale_surface_to_size(image, (800, 600)) for image in conv_images]

clocksum.add(clock.tick())

print 'Resizing pygame to thumbs'

pythumb_images = [enigmage.fit_surface_to_thumb(image) for image in conv_images]

clocksum.add(clock.tick())

#~ print 'Resizing pygame fullscreen to thumbs'
#~ 
#~ pyfullthumb_images = [enigmage.fit_surface_to_thumb(image) for image in pyfull_images]

#~ clocksum.add(clock.tick())

clocksum.total()

print '---------------------------'
print 'Loading PIL'

pil_images = [Image.open(path) for path in paths]

clocksum.add(clock.tick())

print 'Drafting PIL to fullscreen'

#~ pilfull_images = [image.draft(image.mode, (800, 600)) for image in pil_images]
for image in pil_images:
	image.draft(image.mode, (800, 600))
pilfull_images = pil_images

clocksum.add(clock.tick())

print 'Converting PIL fullscreen to pygame converted via string'

piltopy_images = [pygame.image.fromstring(image.tostring(), image.size, image.mode).convert for image in pilfull_images]

clocksum.add(clock.tick())
clocksum.total()

print '---------------------------'
print 'Loading PIL'

pil_images = [Image.open(path) for path in paths]

clocksum.add(clock.tick())

print 'Resizing PIL to fullscreen'

pilfull_images = [image.resize((800, 600)) for image in pil_images]

clocksum.add(clock.tick())

print 'Converting PIL fullscreen to pygame converted via string'

piltopy_images = [pygame.image.fromstring(image.tostring(), image.size, image.mode).convert for image in pilfull_images]

clocksum.add(clock.tick())
clocksum.total()

print '----------------------------'
print 'Loading PIL'

pil_images = [Image.open(path) for path in paths]

clocksum.add(clock.tick())

print 'Converting PIL fullscreen to pygame converted via string'

piltopy_images = [pygame.image.fromstring(image.tostring(), image.size, image.mode).convert() for image in pil_images]

clocksum.add(clock.tick())

print 'Resizing pygame to fullscreens'

pyfull_images = [enigmage.scale_surface_to_size(image, (800, 600)) for image in piltopy_images]

clocksum.add(clock.tick())

print 'Resizing pygame to thumbs'

pythumb_images = [enigmage.fit_surface_to_thumb(image) for image in piltopy_images]

clocksum.add(clock.tick())

clocksum.total()
