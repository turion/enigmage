#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage.examples"""

import enigmage, pygame

loop = True
debug_clock = pygame.time.Clock()
debug = False

def main_loop(mages_list, keyactions):
	enigmage.tick()
	loopcount = 0
	global loop
	while loop:
		enigmage.tick()
		if debug: print "Ticked: ", debug_clock.tick()
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
		if debug: print "Keys: ", debug_clock.tick()
		for mages in mages_list:
			mages.clear(enigmage.screen,enigmage.background)
			if debug: print "Cleared: ", debug_clock.tick()
			mages.update()
			if debug: print "Updated: ", debug_clock.tick()
			mages.draw(enigmage.screen) # dirtyrects = mages.draw(var.screen)
			if debug: print "Drawed: ", debug_clock.tick()
		pygame.display.flip() # pygame.display.update(dirtyrects)
		if debug: print "Flipped: ", debug_clock.tick()
	enigmage.exit()

def end_main_loop():
	global loop
	loop = False
