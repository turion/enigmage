#! /usr/bin/python
# -*- coding: utf-8 -*-

"""enigmage-Spielwiese
Testing for new enigmage and enigtree components"""

import enigmage.directory

dir = "/home/turion/Fotos/selection enigmage"
eggs = enigmage.directory.MageDirNode(dir)
print eggs.elaborate_str()
