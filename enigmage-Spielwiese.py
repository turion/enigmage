#! /usr/bin/python
# -*- coding: utf-8 -*-

# Zum testen von SQLite, enigtree, enigmage.sql und anderer Funktionen, damit das nachher in enigmage verwendet werden kann


#import sqlite3
#import enigmage.sql
#
#enigmage.sql.init('/home/turion/eniglib/enigmage/sqlite/enigmage-sql')
#
#cursor = enigmage.sql.cursor

#cursor.execute("select tag.id, tag.name from tag, tagging where tag.id = tagging.child_id and tagging.parent_id = ?", (image,))
#for mage in cursor.fetchall():
	#print "Mage ", mage[1], " with id ", mage[0], " is stored in the following files:"
	#for magefile in enigmage.sql.files_of(mage[0]):
		#print "ID: ", magefile[0], ", file: ", magefile[1], " in ", enigmage.sql.full_dir(magefile[0])

#cursor.execute('alter table arrow drop integer')

#cursor.execute('select id, parent_id, child_id, date, coupling from tagging where meta = 0')

#for tagging in cursor.fetchall():
	#print tagging
	#cursor.execute('insert into arrow (id, who, what, name, date, coupling) values (?, ?, ?)', (tag[0], tag[1], 1.0))
#enigmage.sql.connection.commit()

#enigmage.sql.close()



#import os
#
#os.chdir('/home/turion/')
#dir = 'Fotos'
#spam = os.listdir(dir)
#subdirs = []
#files = []
#for eggs in spam:
	#if os.path.isdir(os.path.join(dir, eggs)): subdirs.append(eggs)
	#elif os.path.isfile(os.path.join(dir, eggs)): files.append(eggs)
	#
#
#print 
#for eggs in ["Directories:"] + subdirs + ["Files:"] + files: print eggs

#print os.path.join('/home/turion', '/Fotos')

#import enigtree.directory

#class TestDirNode(enigtree.directory.DirNode):
	#def child_accepted(self, child):
		#print child
		#full_child_path = os.path.join(self.path, child)
		#if os.path.isfile(full_child_path):
			#print 'Datei'
			#if child[-4:] in ('.JPG', '.jpg', 'jpeg', 'JPEG'):
				#print 'darf:', full_child_path
				#return True
			#else:
				#print 'darf nicht:', full_child_path			
		#elif os.path.isdir(full_child_path):
			#return True
		#else:
			#return False
#

#import enigmage.directory
#
#eggs = enigmage.directory.MageDirNode(dir)
#
#print eggs
#for egg in eggs.childs:
	#print "-", egg
	#for ham in egg.childs:
		#print "--", ham
		#for bacon in ham.childs:
			#print "---", bacon

#for subegg in eggs.progeny(1):
	#print subegg


import sqlalchemy, sqlalchemy.orm
import sqlite3
import datetime

engine = sqlalchemy.create_engine('sqlite:////home/turion/eniglib/enigmage/sqlite/enigmage-sql', module=sqlite3.dbapi2)

class Tag(object):
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return "<Tag('%s')>" % (self.name)

class Arrow(object):
	def __init__(self, who, how, what, name, coupling, date_time=None):
		self.who = who
		self.how = how
		self.what = what
		if not date_time: date_time = datetime.now()
		self.date = date_time
		self.name = name
		self.coupling = coupling

class Tagging(object):
	pass

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

metadata = sqlalchemy.MetaData(bind=engine)

arrow = sqlalchemy.Table('arrow', metadata, autoload=True)
tagging = sqlalchemy.Table('tagging', metadata, autoload=True)

sqlalchemy.orm.mapper(Tagging, tagging)
sqlalchemy.orm.mapper(Arrow, arrow)

for tagging_instance in session.query(Tagging):
	print tagging_instance.id
	
# tagging in arrow rein, aber dabei mit den ids aufpassen

