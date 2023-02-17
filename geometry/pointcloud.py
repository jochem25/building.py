# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Jonathan Van der Gouwe & Maarten Vroegindeweij     *
#*   jonathan@3bm.co.nl & maarten@3bm.co.nl                                *
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


"""This module provides tools to create a pointcloud
"""

__title__= "pointcloud"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/pointcloud.py"


import math, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) #path: PyBuildingSystems
from geometry.point import *
from packages import helper


class PointCloud:
    def __init__(self, points, id=helper.generateID()) -> None:
        self.points = []
        self.id = id

    def __id__(self):
        return f"id:{self.id}"
        
    def __str__(self) -> str:
        return f"{__class__.__name__}({self.points})"