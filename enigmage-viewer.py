#! /usr/bin/python
# -*- coding: utf-8 -*-


import enigraph
import enigmage, enigmage.magefsnode, enigmage.interface

enigmage.init()

scrambled_eggs = enigmage.magefsnode.MageFSNode(enigmage.current_settings.directory)


meinesprites = enigmage.RamificationMages(scrambled_eggs)
#~ FIXME:
	#~ When zooming in to fast, Mage does not immediately stop
	#~ On zooming out, the Node forgets about which children it came from

enigmage.var.tick()
loopcount = 0
import pygame # TODO: Separate layout and graphics by defining an abstract layout.group. At last, modularise the main loop
while True:
	enigmage.var.tick()
	if enigmage.var.time > 1000:
		print("Delay in loop ", loopcount, ":", enigmage.var.time)
	loopcount += 1
	enigmage.interface.handle_events(meinesprites)
	meinesprites.clear(enigmage.graphics.backend.screen,enigmage.graphics.backend.background)
	meinesprites.update()
	meinesprites.draw(enigmage.graphics.backend.screen) # dirtyrects = meinesprites.draw(enigmage.graphics.backend.screen)
	pygame.display.flip() # pygame.display.update(dirtyrects)
