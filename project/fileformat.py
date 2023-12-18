# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
# *   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************


"""This module provides the fileformat class
"""

__title__= "fileformat"
__author__ = "Maarten & Jonathan"
__url__ = "./fileformat/fileformat.py"


import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from geometry.point import Point
from abstract.coordinatesystem import CoordinateSystem
from abstract.vector import Vector3

# [!not included in BP singlefile - end]
class BuildingPy:
    def __init__(self, name=None, number=None):
        self.name: str = name
        self.number: str = number
        self.objects = []
        self.units = "mm"
        self.decimals = 3 #not fully implemented yet
        self.origin = Point(0,0,0)
        self.default_font = "calibri"
        self.scale = 1000
        self.font_height = 500
        #prefix objects (name)
        #Geometry settings

        #export selection info
        self.domain = None
        self.applicationId = "OPEN-AEC | BuildingPy"

        #different settings for company's?

        #rename this to autoclose?
        self.closed: bool = False #auto close polygons? By default true, else overwrite
        self.round: bool = False #If True then arcs will be segmented. Can be used in Speckle.

        #nodes
        self.node_merge = True #False not yet created
        self.node_diameter = 250
        self.node_threshold = 50
        
        #text
        self.createdTxt = "has been created"

        #Speckle settings
        self.speckleserver = "speckle.xyz"
        self.specklestream = None

        #FreeCAD settings

        XAxis = Vector3(1, 0, 0)
        YAxis = Vector3(0, 1, 0)
        ZAxis = Vector3(0, 0, 1)
        self.CSGlobal = CoordinateSystem(Point(0, 0, 0), XAxis, YAxis, ZAxis)

    # @property
    # def units(self):
    #     return "mm"

# [!not included in BP singlefile - start]
    # def deserialize_point(serialized_point):
    #     data = json.loads(serialized_point)
    #     return Point(data['x'], data['y'], data['z'])

    # def deserialize_line(serialized_line):
    #     data = json.loads(serialized_line)
    #     start_point = deserialize_point(json.dumps(data['start']))
    #     end_point = deserialize_point(json.dumps(data['end']))
    #     return Line(start_point, end_point)
        
    def save(self):
        print(self.objects)
        pass #save all objects in here

    def open(self):
        pass #open data.json objects in here

    def toSpeckle(self, streamid, commitstring=None):
        from exchange.speckle import translateObjectsToSpeckleObjects, TransportToSpeckle
        self.specklestream = streamid
        speckleobj = translateObjectsToSpeckleObjects(self.objects)
        TransportToSpeckle(self.speckleserver,streamid,speckleobj,commitstring)

    def toFreeCAD(self):
        from exchange.freecad_bupy import translateObjectsToFreeCAD
        translateObjectsToFreeCAD(self.objects)
# [!not included in BP singlefile - end]

project = BuildingPy("Project","0")