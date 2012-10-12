#! /usr/bin/python
# -*- coding: utf-8 -*-

from .. import physics, var

class Model(physics.Model):
	def _attraction(self):
		strength = 0.00003

		#weak_scale = 10 # Pixels
		#anharmonicity = + 0.000005		
		#bumpsize = 30 # Pixels
		#bumpheight = 0
		
		snap = 2 # Pixels
		distance = self.mage._target - (self.mage.rect.centerx + 
		self.mage.rect.centery * 1.0j) # TODO sollte _target wirklich beim mage bleiben?
		#self._velocity += strength * distance * math.atan(abs(distance)/weak_scale) / (0.0001 + abs(distance))
		#print (1 + anharmonicity * (abs(distance)**2))
		#self._velocity += var.time * strength * distance * (1 + anharmonicity * (abs(distance)**2))
		#self._velocity += var.time * strength * distance * (1 + bumpheight / (1 + (abs(distance)/bumpsize)**2))
		self._velocity += var.time * strength * distance
		if abs(distance) < snap:
			self._goingto = False
			#print "Went to"
	def _friction(self):
		overall_friction = 0.003 # TODO Das könnten Klassenattribute sein
		ground_friction = 1
		air_friction = 2
		self._velocity -= var.time * overall_friction * self._velocity * (air_friction + ground_friction/(1+abs(self._velocity)))
	def update(self):
		debugstring = str(self) + ' bei ' + str(self.mage.rect.center) + ' v=' + str(self._velocity) # TODO debuginformation per Modul logging
		if not self.mage._show_as_fullscreen: # Doing the physics for the thumb moving
			if self._goingto:
				self._attraction()
				debugstring += ' v+adt=' + str(self._velocity)
			self._friction()
			debugstring += ' v+fdt=' + str(self._velocity) + ' dt=' + str(var.time)
			self._move += self._velocity*var.time
			move = int(round(self._move.real)), int(round(self._move.imag))
			self._move -= move[0] + move[1]*1j # TODO: Die Berechnung wurde doch grad eben schon gemacht
			#if self._goingto: print debugstring
			#if self._blowing: self._blowstep()
			return move
		else:
			return super().update()
