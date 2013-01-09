#! /usr/bin/python
# -*- coding: utf-8 -*-

__ALL__ = ["handle_events"]

import pygame

def init():
	pygame.init()

def handle_events(mages):
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: exit()
			if event.key == pygame.K_RIGHT: mages.focus_successor()
			if event.key == pygame.K_LEFT: mages.focus_predecessor()
			if event.key == pygame.K_DOWN: mages.zoom_in()
			if event.key == pygame.K_UP: mages.zoom_out()
	# events.pump oder so?
	keys = pygame.key.get_pressed()
