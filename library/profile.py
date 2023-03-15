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


"""This module provides tools to get profiledata from the database. These are json files
"""

__title__= "profile"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/profile.py"

import sys, os, math
from pathlib import Path
import json
import urllib.request

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from packages import helper
from objects.shape import *

jsonFile = "https://raw.githubusercontent.com/3BMLabs/building.py/main/library/profile_database/steelprofile.json"
url = urllib.request.urlopen(jsonFile)
data = json.loads(url.read())

class searchProfile:
    def __init__(self, name):
        self.name = name
        self.shape_coords = None
        self.shape_name = None
        self.synonyms = None
        for item in data:
            for i in item.values():
                synonymList = i[0]["synonyms"]
                if self.name in synonymList:
                    self.shape_coords = i[0]["shape_coords"]
                    self.shape_name = i[0]["shape_name"]
                    self.synonyms = i[0]["synonyms"]

class profiledataToShape:
    def __init__(self, name1):
        profile_data = searchProfile(name1)
        shape_name = profile_data.shape_name
        name = profile_data.name
        self.d1 = profile_data.shape_coords
        #self.d1.insert(0,name)
        d1 = self.d1
        if shape_name == "C-channel parallel flange":
            prof = CChannelParallelFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6])
        elif shape_name == "C-channel sloped flange":
            prof = CChannelSlopedFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6],d1[7],d1[8])
        elif shape_name == "I-shape parallel flange":
            prof = IShapeParallelFlange(name,d1[0],d1[1],d1[2],d1[3],d1[4])
        elif shape_name == "Rectangle":
            prof = Rectangle(name,d1[0], d1[1])
        elif shape_name == "Round":
            prof = Round(name)
        elif shape_name == "LAngle":
            prof = LAngle(name,d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6],d1[7])
        elif shape_name == "Rectangle hollow section":
            prof = RectangleHollowSection(name,d1[0],d1[1],d1[2],d1[3],d1[4])
        else:
            prof = "error, profile not created"
        self.prof = prof
        self.data = d1
