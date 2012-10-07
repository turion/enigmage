#! /usr/bin/python
# -*- coding: utf-8 -*-


import enigraph
import enigmage, enigmage.magefsnode

import os, sys


os.chdir('/')
dir = os.path.expanduser('~') + '/Fotos/selection enigmage/'
settings_file_path = os.path.join(dir, '.enigmage')
if os.path.exists(settings_file_path):
	if os.path.isfile(settings_file_path):
		with open(settings_file_path) as settings_file:
			dir = settings_file.readline()[:-1] # TODO Da gibt es doch bessere Wege, eine Einstellungsdatei auszulesen
			fullscreen = settings_file.readline()
	else:
		print("You messed up with .enigmage!")
		fullscreen = False
else:
	print("Please create .enigmage!")
	fullscreen = False
	

#maxbildversize = 300 # TODO was sollte das?


enigmage.init(fullscreen=fullscreen)

scrambled_eggs = enigmage.magefsnode.MageFSNode(dir)


meinesprites = enigmage.RamificationMages(scrambled_eggs)
#~ FIX:
	#~ When zooming in to fast, Mage does not immediately stop
	#~ On zooming out, the Node forgets about which children it came from

enigmage.var.tick()
loopcount = 0
while True:
	enigmage.var.tick()
	if enigmage.var.time > 1000:
		print("Delay in loop ", loopcount, ":", enigmage.var.time)
	loopcount += 1
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: sys.exit()
			if event.key == pygame.K_RIGHT: meinesprites.focus_successor()
			if event.key == pygame.K_LEFT: meinesprites.focus_predecessor()
			if event.key == pygame.K_DOWN: meinesprites.zoom_in()
			if event.key == pygame.K_UP: meinesprites.zoom_out()
	# events.pump oder so?
	keys = pygame.key.get_pressed()
	meinesprites.clear(enigmage.graphics.backend.screen,enigmage.graphics.backend.background)
	meinesprites.update()
	meinesprites.draw(enigmage.graphics.backend.screen) # dirtyrects = meinesprites.draw(var.screen)
	pygame.display.flip() # pygame.display.update(dirtyrects)
