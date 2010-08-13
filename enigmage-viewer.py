#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
enigmage-viewer.py
 
Das eigentliche Programm

Bereits geschafft:
1.Sprites ausprobieren
	Event loop, verwende gescheites timing
2.Bilder verschieben
3a Mage
	Bewegung flüssig mit target und friction
	Zoom in/Zoom out bzw. Fullscreen/Thumb
3b. Mehrere Bilder gleichzeitig
	Eigene Gruppe
4z. Nodes statt:
	Virtuelle Verzeichnisse, MageDirectory Klasse
		aktives Verzeichnis mit Grundfunktionen zur Kommunikation mit einer Bildschirmgruppe

Aktuell:

4a. Dateiverwaltung
	Via Nodes...
		Unterklassen davon, die tatsächlich etwas können, z.B. SQL, Dateisystem
			"SQLMageNode" oder so durch und durch Objektorientiert
				SQL-Daten nicht in data ablegen wegen Seit-/Abwärtskompatibilität
				Alchemy richtig in den Griff kriegen
		Selbstständiger DirectoryNode
		Davon eine Unterklasse, die automatisch die Mages lädt?
			Es fehlt noch Schreibzugriff

7. Performance verbessern
		Multithreading
			Hintergrundprozess, der Thumbs erstellt und Bilder vorlädt usw.
				Den braucht man jetzt schon, damit es benutzbar wird
				Den Prozess beim initialisieren in Var einbauen?
				Zum Beschleunigen nicht alles laden
					Spezielle Bibliothek verwenden
		Nur die Mages anzeigen, die im Bildbereich sind! (Brauche ich das jetzt schon? Mal testen.)
			Unbenutzte Mages aus dem Speicher löschen
			Am besten diese Funktion schon in Mages einbauen? Das wird kompliziert! Wobei, eigentlich ist es einfach?


Noch zu tun:
4a. Dateiverwaltung
	Schreibzugriff
4b. SQL
		Tags
			Nicht nur Baumstruktur, sondern Mitgliedschaft in mehreren Gruppen via hierarchischer Tags
			Hierarchie der Tags über tag_hierarchy ist mengenartig (ein Tag kann mehrere Übertags haben) und ausschließlich direkt (nicht transitiv: Tag3 Übertag für Tag2 und Tag 2 Übertag für Tag1 führt nicht dazu, dass Tag3 Übertag für Tag1. Man kann diese Struktur aber trotzdem baumartig benutzen.)
			Tagzugehörigkeit wird durch Coupling quantifiziert
				Rating geschieht durch Tags (z.B. tag "kalenderhaft", "gut", "überbelichtet") und coupling
5. Alles zusammenstecken
		Gedanken wegen Packages machen, vielleicht main() implementieren
		Einstellungsdatei ausbauen
			Die Einstellungsdatei sollte eine normale Pythondatei sein, die auf globale Variablen in enigmage-viewer.py zugreifen kann
6. Praktische Funktionen einbauen/ Eyecandy
		"Einsortieren": Zwei Gruppen, eine links im halben Fullscreen die neuen Fotos durchblätternd, die rechts in einen Baum einsortiert werden
		MageLabelled
		LayeredUpdates anstatt Group verwenden um Überlappungen in den Griff zu bekommen
		Baumartige Gruppen
		Dateien nicht nur lesen, sondern auch schreiben
			DirNode so bauen, dass er schreibbare Eigenschaften hat
				Vielleicht auch dafür einen Hintergrundprozess starten
7. Performance verbessern
		Mages nur einmal laden, Überprüfung durch Gruppenzugehörigkeit
		Bilder außerhalb der Sichtbereiches nicht zeichnen
		DirtyRects
		done
		Multithreading
			Hintergrundprozess, der Thumbs erstellt und Bilder vorlädt usw.
8. Weitere Funktionen
		OpenGL-Backend
		Ideen in Wikistruktur
		TeX-Snippets in der Datenbank, per dvipng ausgeben
			Bibliothekabhängigkeiten in der Datenbank verzeichnen
		Backups der Datenbank in lesbaren Formaten (SQL? HTML??)
"""

import enigmage, enigtree, enigmage.directory

import os, sys, pygame

pygame.init()

os.chdir('/')
dir = os.path.expanduser('~') + '/'
settings_file_path = os.path.join(dir, '.enigmage')
if os.path.exists(settings_file_path):
	if os.path.isfile(settings_file_path):
		with open(settings_file_path) as settings_file:
			dir = settings_file.readline()[:-1]
			fullscreen = settings_file.readline()
	else:
		print "You messed up with .enigmage!"
else:
	print "Please create .enigmage!"
	

maxbildversize = 300

if fullscreen == 'yes':
	size = 1024, 768
	screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
	size = 800, 600
	screen = pygame.display.set_mode(size)

enigmage.init(screen)

	
#~ scrambled_eggs = enigmage.directory.MageDirNode(dir)

import enigmage.loader
scrambled_eggs = enigmage.loader.LazyMageDirNode(dir)


meinesprites = enigmage.RamificationMages(screen.get_rect(), scrambled_eggs)

import random, pygame.time

enigmage.var.tick()
loopcount = 0
while True:
	#~ with enigmage.loop_lock:
	enigmage.var.tick()
	if enigmage.var.time > 100: print "Delay in loop ", loopcount, ":", enigmage.var.time, "milliseconds"
	loopcount += 1
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				enigmage.loader.mage_loader.pickup_job(enigmage.job.TermJob(priority=3)) # Wieso bringt das nix?
				enigmage.quit()
				sys.exit()
			if event.key == pygame.K_RIGHT: meinesprites.focus_successor()
			if event.key == pygame.K_LEFT: meinesprites.focus_predecessor()
			if event.key == pygame.K_DOWN: meinesprites.zoom_in()
			if event.key == pygame.K_UP: meinesprites.zoom_out()
			if event.key == pygame.K_d: scrambled_eggs.childs[0].data.dance()
	# events.pump oder so?
	keys = pygame.key.get_pressed()
	meinesprites.clear(enigmage.var.screen,enigmage.var.background)
	meinesprites.update() # Bastian: ja, nur dass man diese schritte nochmal für die Physik unterteilt
	meinesprites.draw(enigmage.var.screen) # dirtyrects = meinesprites.draw(var.screen)
	pygame.display.flip() # pygame.display.update(dirtyrects)

