
#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage-Spielwiese
Testing for new enigmage and enigtree components"""

import enigtree

parent = enigtree.Node(data="Elternteil")

child1 = enigtree.Node(parent=parent, data="Großer Bruder")
child2 = enigtree.Node(parent=parent, data="Kleine Schwester")

enkel = enigtree.Node(parent=child1, data="Kleener")
enkel2 = enigtree.Node(parent=child2, data="Der andere Kleene")
urenkel = enigtree.Node(parent=enkel, data="Der ganz Kleene")

print("{} sagt: Mein Nachfolger ist {}".format(child1, child2))
print(parent.elaborate_str())
