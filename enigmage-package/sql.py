#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage.sql
Basic SQL functionalities. Hopefully this file will become backend independent."""

import sqlite3

def setting(setting_keyword):
	cursor.execute('select tag.id from tag where tag.name = ?', (setting_keyword,))
	result = cursor.fetchone()
	assert result
	return result[0]

def init(database_path):
	global connection, cursor, settings
	connection = sqlite3.connect(database_path)
	cursor = connection.cursor()
	setting_keywords = ['folder', 'image', 'file', 'group', 'person', 'visible', 'shot']
	settings = dict([(setting_keyword, setting(setting_keyword)) for setting_keyword in setting_keywords])

def full_dir(file_id):
	cursor.execute('select tag.name, tag.id from tag, tagging as is_path_tagging, tagging as containing_tagging where tag.id = containing_tagging.parent_id and containing_tagging.child_id = ? and is_path_tagging.child_id = tag.id and is_path_tagging.parent_id = ?', (file_id, settings['folder']))
	containing_folder = cursor.fetchone()
	if containing_folder:
		#print "Going on, found ", containing_folder[0]
		result = full_dir(containing_folder[1]) + containing_folder[0]
	else:
		#print "stopped"
		result = ''
	return result

def files_of(mage_id):
	"""returns all file instances of a given mage in a list of tuples (id, name)"""
	cursor.execute('select tag.id, tag.name from tag, tagging as is_file_tagging, tagging where tag.id = tagging.child_id and tag.id = is_file_tagging.child_id and is_file_tagging.parent_id = ? and tagging.parent_id = ?', (settings['file'],mage_id))
	return cursor.fetchall()

def close(commit=True):
	"""Closes the connection but automatically commits before doing so."""
	if commit:
		connection.commit()
	connection.close()
	
# The next one is not yet tested:

def add_couplings(id, tag_id=None, tag_name=None):
	if not (tag_id or tag_name):
		raise sqlite3.Error("Insufficient id or data provided")
	parents = [(id, 1)]
	while parents:
		parent = parents.pop()
		# Handle tag_id = None!
		cursor.execute('select tagging.parent_id, tagging.coupling from tagging, tagging as is_group, tagging as is_tag where tagging.child_id = ?, is_group.child_id = ?, is_group.parent_id = ?, is_tag.child_id = ?, is_tag.parent_id = ?', (parent[0], parent[0], settings["group"], parent[0], tag_id))
		for grandparent in cursor.fetchall():
			parents.append((grandparent[0], grandparent[1]*parent[1]))
	all_couplings = [parent[1] for parent in parents]
	# sum all couplings and return!


