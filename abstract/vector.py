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


"""This module provides tools for vectors
"""

__title__= "vector"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/vector.py"

import math
import sys, random
from pathlib import Path
file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.point import *

from packages import helper

class Vector3:
    def __init__(self, x, y, z):
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0

        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def sum(v1, v2):
        return Vector3(
            v1.x + v2.x,
            v1.y + v2.y,
            v1.z + v2.z
        )

    @staticmethod
    def diff(v1, v2):
        return Vector3(
            v1.x - v2.x,
            v1.y - v2.y,
            v1.z - v2.z
        )

    @staticmethod
    def divide(v1, v2):
        return Vector3(
            v1.x / v2.x,
            v1.y / v2.y,
            v1.z / v2.z
        )


    @staticmethod
    def square(v1):
        return Vector3(
            v1.x **2,
            v1.y **2,
            v1.z **2
        )


    @staticmethod
    def toPoint(v1):
        from geometry.point import Point
        return Point(x=v1.x,y=v1.y,z=v1.z)


    @staticmethod
    def toLine(v1, v2):
        from geometry.point import Point
        from geometry.curve import Line
        return Line(start = Point(x=v1.x,y=v1.y,z=v1.z), end = Point(x=v2.x,y=v2.y,z=v2.z))

    @staticmethod
    def byLine(l1):
        from geometry.curve import Line
        return Vector3(l1.dx,l1.dy,l1.dz)

    @staticmethod
    def lineByLength(v1, length:float):
        from geometry.point import Point
        from geometry.curve import Line
        return Line(start = Point(x=v1.x,y=v1.y,z=v1.z), end = Point(x=v2.x,y=v2.y,z=v2.z))
    

    @staticmethod #Returns vector perpendicular on the two vectors
    def crossProduct(v1, v2):
        return Vector3(
            v1.y*v2.z - v1.z*v2.y,
            v1.z*v2.x - v1.x*v2.z,
            v1.x*v2.y - v1.y*v2.x
        )

    @staticmethod #inwendig product, if zero, then vectors are perpendicular
    def dotProduct(v1, v2):
        return v1.x*v2.x+v1.y*v2.y+v1.z*v2.z

    @staticmethod
    def product(n, v1): #Same as scale
        return Vector3(
            v1.x*n,
            v1.y*n,
            v1.z*n
        )

    @staticmethod
    def length(v1):
        return math.sqrt(v1.x*v1.x+v1.y*v1.y+v1.z*v1.z)

    @staticmethod
    def pitch(v1, angle):
        return Vector3(
            v1.x,
            v1.y*math.cos(angle) - v1.z*math.sin(angle),
            v1.y*math.sin(angle) + v1.z*math.cos(angle)
        )

    @staticmethod
    def angleBetween(v1, v2):
        return math.degrees(math.acos((Vector3.dotProduct(v1, v2)/(Vector3.length(v1)*Vector3.length(v2)))))
    
    @staticmethod
    def angleRadianBetween(v1, v2):
        return math.acos((Vector3.dotProduct(v1, v2)/(Vector3.length(v1)*Vector3.length(v2))))

    @staticmethod
    def reverse(v1):
        return Vector3(
            v1.x*-1,
            v1.y*-1,
            v1.z*-1
        )

    @staticmethod
    def perpendicular(v1):
        #Vector Lokale x en Lokale y haaks op gegeven vector en in globale z-richting.
        lokX = Vector3(v1.y, -v1.x, 0)
        lokZ = Vector3.crossProduct(v1, lokX)
        if lokZ.z<0:
            lokZ = Vector3.reverse(lokZ)
        return lokX, lokZ

    @staticmethod
    def normalise(v1):
        scale = 1/Vector3.length(v1)
        return Vector3(
            v1.x*scale,
            v1.y*scale,
            v1.z*scale
        )

    @staticmethod
    def byTwoPoints(p1, p2):
        return Vector3(
            p2.x-p1.x,
            p2.y-p1.y,
            p2.z-p1.z
        )

    @staticmethod
    def rotateXY(v1, Beta):
        return Vector3(
            math.cos(Beta)*v1.x - math.sin(Beta)*v1.y,
            math.sin(Beta)*v1.x + math.cos(Beta)*v1.y,
            v1.z
        )

    @staticmethod
    def scale(v1, scalefactor):
        return Vector3(
            v1.x * scalefactor,
            v1.y * scalefactor,
            v1.z * scalefactor
        )

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.x},{self.y},{self.z})"


XAxis = Vector3(1, 0, 0)

YAxis = Vector3(0, 1, 0)

ZAxis = Vector3(0, 0, 1)