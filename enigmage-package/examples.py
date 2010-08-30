#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage.examples"""

import enigmage, pygame

loop = True
def main_loop(mages_list, keyactions):
	enigmage.tick()
	loopcount = 0
	global loop
	while loop:
		enigmage.tick()
		if enigmage.time > 100:
			print "Delay in loop ", loopcount, ":", enigmage.time, "milliseconds"
		loopcount += 1
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				try:
					keyactions[event.key]()
				except KeyError:
					pass
		# events.pump oder so?
		# keys = pygame.key.get_pressed() gibts auch
		for mages in mages_list:
			mages.clear(enigmage.screen,enigmage.background)
			mages.update()
			mages.draw(enigmage.screen) # dirtyrects = mages.draw(var.screen)
		pygame.display.flip() # pygame.display.update(dirtyrects)
	enigmage.exit()

def end_main_loop():
	global loop
	loop = False
