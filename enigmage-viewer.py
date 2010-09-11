#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
enigmage-viewer.py --- Example
"""

import enigmage, enigmage.directory, sys, os.path

try:
	dir = sys.argv[1]
except IndexError:
	dir = os.path.expanduser('~')
go_fullscreen = False

if go_fullscreen:
	size = 1024, 768
else:
	size = 800, 600
enigmage.init(size, go_fullscreen)
	
scrambled_eggs = enigmage.directory.MageDirNode(dir)

meinesprites = enigmage.RamificationMages(scrambled_eggs, enigmage.screen.get_rect())

import enigmage.examples, pygame

keyactions= { pygame.K_ESCAPE: enigmage.examples.end_main_loop,
	pygame.K_RIGHT: meinesprites.focus_successor,
	pygame.K_LEFT: meinesprites.focus_predecessor,
	pygame.K_DOWN: meinesprites.zoom_in,
	pygame.K_RETURN: meinesprites.zoom_in,
	pygame.K_UP: meinesprites.zoom_out,
	pygame.K_d: meinesprites.dance
}

enigmage.examples.main_loop([meinesprites], keyactions)
