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


"""This module provides tools for text
"""

__title__= "text"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/text.py"


import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from exchange.speckle import *
from geometry.point import *
from abstract.vector import *
from abstract.coordinatesystem import *
from abstract.boundingbox import *
from geometry.solid import *
from geometry.geometry2d import *

from svg.path import parse_path
import json
from typing import List, Tuple

class Text:
    def __init__(self, text: str = None, font_family: str = None, cs= None ,xyz: Point = None, v: Vector3 = None):
        self.text = text
        self.font_family = font_family or "arial"
        self.xyz = xyz
        self.csglobal = cs or CSGlobal
        self.x, self.y, self.z = xyz.x, xyz.y, xyz.z
        self.v = v
        self.character_offset = 150
        self.space = 850
        self.path_list = self.load_path()


    def load_path(self) -> List[str]:
        with open(f'C:/Users/mikev/Documents/GitHub/building.py/library/text/json/{self.font_family}.json', 'r') as f:
            glyph_data = json.load(f)
            output = []
            for letter in self.text:
                if letter in glyph_data:
                    output.append(glyph_data[letter]["glyph-path"])
                elif letter == " ":
                    output.append("space")
            return output


    def write(self) -> List[List[PolyCurve]]:
        output_list = []
        for letter_path in self.path_list:
            points = []
            allPoints = []
            if letter_path == "space":
                self.x += self.space + self.character_offset
                pass
            else:
                path = parse_path(letter_path)
                for segment in path:
                    segment_type = segment.__class__.__name__
                    if segment_type == 'Move':
                        if len(points) > 0:
                            points = []
                            allPoints.append("M")
                        subpath_started = True
                    elif subpath_started:
                        if segment_type == 'Line':
                            points.extend([(segment.start.real, segment.start.imag), (segment.end.real, segment.end.imag)])
                            allPoints.extend([(segment.start.real, segment.start.imag), (segment.end.real, segment.end.imag)])
                        elif segment_type == 'CubicBezier':
                            points.extend(segment.sample(10))
                            allPoints.extend(segment.sample(10))
                        elif segment_type == 'QuadraticBezier':
                            for i in range(11):
                                t = i / 10.0
                                point = segment.point(t)
                                points.append((point.real, point.imag))
                                allPoints.append((point.real, point.imag))
                        elif segment_type == 'Arc':
                            points.extend(segment.sample(10))
                            allPoints.extend(segment.sample(10))
                if points:
                    output_list.append(self.convert_points_to_polyline(allPoints))
                    width = self.calculate_bounding_box(allPoints)[1]
                    self.x += width + self.character_offset

        pList = []
        for ply in flatten(output_list):
            self.translate(ply)
            pList.append(ply)

        print(f'Object text naar objects gestuurd.')
        return pList


    def translate(self, polyCurve):
        trans = []
        for pt in polyCurve.points:
            pNew = transformPoint(pt, self.csglobal, self.xyz, self.v)
            trans.append(pNew)
        project.objects.append(polyCurve.byPoints(trans))


    def calculate_bounding_box(self, points):
        points = [elem for elem in points if elem != 'M']
        ptList = [Point2D(pt[0], pt[1]) for pt in points]
        bounding_box_polyline = BoundingBox2d().byPoints(ptList)
        return bounding_box_polyline, bounding_box_polyline.width, bounding_box_polyline.height


    def convert_points_to_polyline(self, points: list[Point]) -> PolyCurve: #move
        output_list = []
        sub_lists = [[]]
        tempPoints = [elem for elem in points if elem != 'M']
        x_values = [point[0] for point in tempPoints]
        y_values = [point[1] for point in tempPoints]

        xmin = min(x_values)
        ymin = min(y_values)

        for item in points:
            if item == 'M':
                sub_lists.append([])
            else:
                x = item[0] + self.x - xmin
                y = item[1] + self.y - ymin
                z = self.xyz.z
                eput = x, y, z
                sub_lists[-1].append(eput)
        output_list = [[Point(point[0], point[1], self.xyz.z) for point in element] for element in sub_lists]

        polyline_list = [
            PolyCurve.byPoints([Point(coord.x, coord.y, self.xyz.z) for coord in pts])
            for pts in output_list
        ]
        return polyline_list
