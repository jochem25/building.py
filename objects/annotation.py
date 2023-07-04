# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
#*   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

from geometry.point import *
from geometry.curve import *
"""This module provides tools for analytical element like supports, loads
"""

__title__= "annotation"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/annotation.py"

class Dimension:
    def __init__(self, start: Point, end: Point) -> None:
        self.start: Point = start
        self.end: Point = end
        self.id = helper.generateID()
        self.scale = 0.01

    def geom:

class DimensionType:
    def __init__(self):
        self.name: Point = None
        self.id = helper.generateID()
        self.font = None
        self.
class
class Label:
class LabelType:
class Text:
class TextType: