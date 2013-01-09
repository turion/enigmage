#! /usr/bin/python
# -*- coding: utf-8 -*-

def init():
	from . import pygame as backend
	global backend
	backend.init()

def handle_events(*args, **kwargs): # Muss auch nicht sein
	backend.handle_events(*args, **kwargs)
