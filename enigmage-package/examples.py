#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage.examples"""

import enigmage, pygame

import pygame.time

debug_clock = pygame.time.Clock()
loop = True
loop_lock = False
def main_loop(mages_list, keyactions):
	enigmage.tick()
	loopcount = 0
	global loop
	global loop_lock
	while loop:
		loop_lock = False
		enigmage.tick()
		print "Ticked: ", debug_clock.tick()
		loop_lock = True
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
		print "Keys: ", debug_clock.tick()
		for mages in mages_list:
			mages.clear(enigmage.screen,enigmage.background)
			print "Cleared: ", debug_clock.tick()
			mages.update()
			print "Updated: ", debug_clock.tick()
			mages.draw(enigmage.screen) # dirtyrects = mages.draw(var.screen)
			print "Drawed: ", debug_clock.tick()
		pygame.display.flip() # pygame.display.update(dirtyrects)
		print "Flipped: ", debug_clock.tick()
	enigmage.exit()

def end_main_loop():
	global loop
	loop = False
