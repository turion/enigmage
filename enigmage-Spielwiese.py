#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage-Spielwiese
Testing for enigmage components"""

#Teste den PriorityJobster ausführlich!

import enigmage.job, time

print 'Jetzt lade ich den priorityjobster.'

loader = enigmage.job.PriorityJobster(time_per_loop=1000)

print 'Jetzt starte ich ihn.'

loader.start()

print 'Jetzt warte ich.'

time.sleep(2.5)

print 'Jetzt erzeuge ich den termjob.'

termjob = enigmage.job.TermJob(hara="kiri")

print 'Jetzt schieße ich den Vogel ab.'

loader.pickup_job(termjob)

print 'Jetzt warte ich auf ihn.'

loader.join()

print 'Das wars.'

