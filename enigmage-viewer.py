#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
enigmage-viewer.py --- Example
"""

import enigmage, enigtree, enigmage.directory

import os, pygame

pygame.init()

dir = "/home/turion/Fotos/selection enigmage/"
go_fullscreen = False

if go_fullscreen:
	size = 1024, 768
else:
	size = 800, 600
enigmage.init(size, go_fullscreen)

	
#~ scrambled_eggs = enigmage.directory.MageDirNode(dir)

import enigmage.loader
scrambled_eggs = enigmage.loader.LazyMageDirNode(dir)


meinesprites = enigmage.RamificationMages(scrambled_eggs, enigmage.var.screen.get_rect())

enigmage.var.tick()
loopcount = 0
loop = True
while loop:
	#~ with enigmage.loop_lock:
	enigmage.var.tick()
	if enigmage.var.time > 100: print "Delay in loop ", loopcount, ":", enigmage.var.time, "milliseconds"
	loopcount += 1
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: loop = False
			if event.key == pygame.K_RIGHT: meinesprites.focus_successor()
			if event.key == pygame.K_LEFT: meinesprites.focus_predecessor()
			if event.key == pygame.K_DOWN: meinesprites.zoom_in()
			if event.key == pygame.K_UP: meinesprites.zoom_out()
			if event.key == pygame.K_d: meinesprites.dance()
	# events.pump oder so?
	keys = pygame.key.get_pressed()
	meinesprites.clear(enigmage.var.screen,enigmage.var.background)
	meinesprites.update()
	meinesprites.draw(enigmage.var.screen) # dirtyrects = meinesprites.draw(var.screen)
	pygame.display.flip() # pygame.display.update(dirtyrects)

enigmage.exit()
