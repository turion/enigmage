#! /usr/bin/python
# -*- coding: utf-8 -*-

class BaseSettings:
	def __init__(self, fullscreen=False):
		self.fullscreen = fullscreen
		self.directory = ""

class FileSettings(BaseSettings):
	def __init__(self, settings_file_dir="~"):
		import os, os.path
		os.chdir('/')
		settings_file_dir = os.path.expanduser(settings_file_dir)
		
		#default values:
		self.directory = settings_file_dir
		self.fullscreen = False
		
		settings_file_name = os.path.join(settings_file_dir, '.enigmage')
		if os.path.exists(settings_file_name):
			try:
				with open(settings_file_name) as settings_file:
					self.directory = settings_file.readline()[:-1] # TODO Da gibt es doch bessere Wege, eine Einstellungsdatei auszulesen
					self.fullscreen = settings_file.readline() and True or False
			except IOError:
				print("You messed up with .enigmage!") # TODO: Das sollen Warnings sein
		else:
			print("Please create .enigmage!")

def return_settings():
	return FileSettings()
