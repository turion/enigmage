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
		Selbstständiger DirectoryNode
		Davon eine Unterklasse, die automatisch die Mages lädt?
	os.path verwenden

Noch zu tun:
4a. Dateiverwaltung
4b. SQL
		Tags
			Nicht nur Baumstruktur, sondern Mitgliedschaft in mehreren Gruppen via hierarchischer Tags
			Hierarchie der Tags über tag_hierarchy ist mengenartig (ein Tag kann mehrere Übertags haben) und ausschließlich direkt (nicht transitiv: Tag3 Übertag für Tag2 und Tag 2 Übertag für Tag1 führt nicht dazu, dass Tag3 Übertag für Tag1. Man kann diese Struktur aber trotzdem baumartig benutzen.)
			Tagzugehörigkeit wird durch Coupling quantifiziert
				Rating geschieht durch Tags (z.B. tag "kalenderhaft", "gut", "überbelichtet") und coupling

5. Alles zusammenstecken
		Gedanken wegen Packages machen, vielleicht main() implementieren
6. Praktische Funktionen einbauen/ Eyecandy
		"Einsortieren": Zwei Gruppen, eine links im halben Fullscreen die neuen Fotos durchblätternd, die rechts in einen Baum einsortiert werden
		MageLabelled
		LayeredUpdates anstatt Group verwenden um Überlappungen in den Griff zu bekommen
		Baumartige Gruppen
		Dateien nicht nur lesen, sondern auch schreiben
7. Performance verbessern
		Mages nur einmal laden, Überprüfung durch Gruppenzugehörigkeit
		Bilder außerhalb der Sichtbereiches nicht zeichnen
		DirtyRects
		done
		Multithreading
			Hintergrundprozess, der Thumbs erstellt und Bilder vorlädt usw.
8. OpenGL-Backend
"""

import enigmage, enigtree, enigmage.directory

import os, sys, pygame, pygame.sprite

pygame.init()

size = 800, 600
maxbildversize = 300
screen = pygame.display.set_mode(size)

enigmage.init(screen)

os.chdir('/')
dir = '/home/turion/Fotos/selection enigmage'
scrambled_eggs = enigmage.directory.MageDirNode(dir)

print scrambled_eggs.elaborate_str()

meinesprites = enigmage.Mages(screen.get_rect(), scrambled_eggs)


enigmage.var.tick()
loopcount = 0
while True:
	enigmage.var.tick()
	if enigmage.var.time > 1000: print "Delay in loop ", loopcount, ":", enigmage.var.time
	loopcount += 1
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: sys.exit()
			if event.key == pygame.K_RIGHT: meinesprites.focus_right()
			if event.key == pygame.K_LEFT: meinesprites.focus_left()
			if event.key == pygame.K_DOWN: meinesprites.zoom_in()
			if event.key == pygame.K_UP: meinesprites.zoom_out()
	# events.pump oder so?
	keys = pygame.key.get_pressed()
	meinesprites.clear(enigmage.var.screen,enigmage.var.background)
	meinesprites.update()
	meinesprites.draw(enigmage.var.screen) # dirtyrects = meinesprites.draw(var.screen)
	pygame.display.flip() # pygame.display.update(dirtyrects)
