#! /usr/bin/python
# -*- coding: utf-8 -*-


import enigraph
import enigmage, enigmage.magefsnode

enigmage.init()

scrambled_eggs = enigmage.magefsnode.MageFSNode(enigmage.current_settings.directory)


meinesprites = enigmage.RamificationMages(scrambled_eggs)
#~ FIXME:
	#~ When zooming in to fast, Mage does not immediately stop
	#~ On zooming out, the Node forgets about which children it came from

enigmage.var.tick()
loopcount = 0
import pygame # TODO Die Mainloop muss noch irgendwohin
while True:
	enigmage.var.tick()
	if enigmage.var.time > 1000:
		print("Delay in loop ", loopcount, ":", enigmage.var.time)
	loopcount += 1
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: exit()
			if event.key == pygame.K_RIGHT: meinesprites.focus_successor()
			if event.key == pygame.K_LEFT: meinesprites.focus_predecessor()
			if event.key == pygame.K_DOWN: meinesprites.zoom_in()
			if event.key == pygame.K_UP: meinesprites.zoom_out()
	# events.pump oder so?
	keys = pygame.key.get_pressed()
	meinesprites.clear(enigmage.graphics.backend.screen,enigmage.graphics.backend.background)
	meinesprites.update()
	meinesprites.draw(enigmage.graphics.backend.screen) # dirtyrects = meinesprites.draw(enigmage.graphics.backend.screen)
	pygame.display.flip() # pygame.display.update(dirtyrects)
