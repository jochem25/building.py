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


"""This module provides classes for 3d objects
"""

__title__ = "shape3d"
__author__ = "Joas"
__url__ = "./objects/shape3d.py"

import sys
import math
from pathlib import Path
from exchange.speckle import *

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))


class Origin:

    def __init__(self):
        self.originx = 0
        self.originy = 0
        self.originz = 0
        self.number_of_triangles = 300
        self.number_of_rectangles = 400
        self.r = 800
        self.r2 = 300
        self.vertices_up = [self.originx, self.originy, self.originz + 350]
        self.vertices_right = [self.originx + 350, self.originy, self.originz]
        self.vertices_front = [self.originx, self.originy + 350, self.originz]
        self.faces_up = []
        self.faces_right = []
        self.faces_front = []
        self.facenr = 1
        self.degrees = 0
        self.degrees2 = 360 / self.number_of_triangles

    # UP ARROW

    def CreateOrigin(self):
        for i in range(self.number_of_triangles):
            x = math.cos(math.radians(self.degrees)) * self.r
            y = math.sin(math.radians(self.degrees)) * self.r
            self.degrees += self.degrees2
            self.vertices_up.append(self.originx + x)
            self.vertices_up.append(self.originy + y)
            self.vertices_up.append(self.originz + 200)

            self.faces_up.append(3)
            self.faces_up.append(0)

            if self.facenr < self.number_of_triangles:
                self.faces_up.append(self.facenr)
                self.faces_up.append(self.facenr + 1)
                self.facenr += 1
            else:
                self.faces_up.append(self.number_of_triangles)
                self.faces_up.append(1)

                self.faces_up.append(self.number_of_triangles)
                for i in range(self.number_of_triangles):
                    self.faces_up.append(i + 1)

        vertices2 = []
        faces2 = []
        facenr2 = 0
        degrees3 = 0
        degrees4 = 360 / self.number_of_rectangles

        for i in range(self.number_of_rectangles):
            x = math.cos(math.radians(degrees3)) * self.r2
            y = math.sin(math.radians(degrees3)) * self.r2
            vertices2.append(self.originx + x)
            vertices2.append(self.originy + y)
            vertices2.append(self.originz + 200)
            vertices2.append(self.originx + x)
            vertices2.append(self.originy + y)
            vertices2.append(self.originz)
            degrees3 += degrees4

            if facenr2 < self.number_of_rectangles * 2 - 2:
                faces2.append(4)
                faces2.append(facenr2)
                faces2.append(facenr2 + 1)
                faces2.append(facenr2 + 3)
                faces2.append(facenr2 + 2)
                facenr2 += 2
            else:
                faces2.append(4)
                faces2.append(facenr2)
                faces2.append(facenr2 + 1)
                faces2.append(1)
                faces2.append(0)

                faces2.append(self.number_of_rectangles)
                count = 1
                for i in range(self.number_of_rectangles):
                    if count <= self.number_of_rectangles * 2:
                        faces2.append(count)
                        count += 2
                    else:
                        pass

        # RIGHT ARROW

        self.degrees = 0
        self.facenr = 1

        for i in range(self.number_of_triangles):
            z = math.cos(math.radians(self.degrees)) * self.r
            y = math.sin(math.radians(self.degrees)) * self.r
            self.degrees += self.degrees2
            self.vertices_right.append(self.originx + 200)
            self.vertices_right.append(self.originy + y)
            self.vertices_right.append(self.originz + z)

            self.faces_right.append(3)
            self.faces_right.append(0)

            if self.facenr < self.number_of_triangles:
                self.faces_right.append(self.facenr)
                self.faces_right.append(self.facenr + 1)
                self.facenr += 1
            else:
                self.faces_right.append(self.number_of_triangles)
                self.faces_right.append(1)

                self.faces_right.append(self.number_of_triangles)
                for i in range(self.number_of_triangles):
                    self.faces_right.append(i + 1)

        vertices_right2 = []
        faces_right2 = []
        facenr2 = 0
        degrees3 = 0
        degrees4 = 360 / self.number_of_rectangles

        for i in range(self.number_of_rectangles):
            z = math.cos(math.radians(degrees3)) * self.r2
            y = math.sin(math.radians(degrees3)) * self.r2
            vertices_right2.append(self.originx + 200)
            vertices_right2.append(self.originy + y)
            vertices_right2.append(self.originz + z)
            vertices_right2.append(self.originx)
            vertices_right2.append(self.originy + y)
            vertices_right2.append(self.originz + z)
            degrees3 += degrees4

            if facenr2 < self.number_of_rectangles * 2 - 2:
                faces_right2.append(4)
                faces_right2.append(facenr2)
                faces_right2.append(facenr2 + 1)
                faces_right2.append(facenr2 + 3)
                faces_right2.append(facenr2 + 2)
                facenr2 += 2
            else:
                faces_right2.append(4)
                faces_right2.append(facenr2)
                faces_right2.append(facenr2 + 1)
                faces_right2.append(1)
                faces_right2.append(0)

                faces_right2.append(self.number_of_rectangles)
                count = 1
                for i in range(self.number_of_rectangles):
                    if count <= self.number_of_rectangles * 2:
                        faces_right2.append(count)
                        count += 2
                    else:
                        pass

        # FRONT ARROW

        self.degrees = 0
        self.facenr = 1

        for i in range(self.number_of_triangles):
            z = math.cos(math.radians(self.degrees)) * self.r
            x = math.sin(math.radians(self.degrees)) * self.r
            self.degrees += self.degrees2
            self.vertices_front.append(self.originx + x)
            self.vertices_front.append(self.originy + 200)
            self.vertices_front.append(self.originz + z)

            self.faces_front.append(3)
            self.faces_front.append(0)

            if self.facenr < self.number_of_triangles:
                self.faces_front.append(self.facenr)
                self.faces_front.append(self.facenr + 1)
                self.facenr += 1
            else:
                self.faces_front.append(self.number_of_triangles)
                self.faces_front.append(1)

                self.faces_front.append(self.number_of_triangles)
                for i in range(self.number_of_triangles):
                    self.faces_front.append(i + 1)

        vertices_front2 = []
        faces_front2 = []
        facenr2 = 0
        degrees3 = 0
        degrees4 = 360 / self.number_of_rectangles

        for i in range(self.number_of_rectangles):
            z = math.cos(math.radians(degrees3)) * self.r2
            x = math.sin(math.radians(degrees3)) * self.r2
            vertices_front2.append(self.originx + x)
            vertices_front2.append(self.originy + 200)
            vertices_front2.append(self.originz + z)
            vertices_front2.append(self.originx + x)
            vertices_front2.append(self.originy)
            vertices_front2.append(self.originz + z)
            degrees3 += degrees4

            if facenr2 < self.number_of_rectangles * 2 - 2:
                faces_front2.append(4)
                faces_front2.append(facenr2)
                faces_front2.append(facenr2 + 1)
                faces_front2.append(facenr2 + 3)
                faces_front2.append(facenr2 + 2)
                facenr2 += 2
            else:
                faces_front2.append(4)
                faces_front2.append(facenr2)
                faces_front2.append(facenr2 + 1)
                faces_front2.append(1)
                faces_front2.append(0)

                faces_front2.append(self.number_of_rectangles)
                count = 1
                for i in range(self.number_of_rectangles):
                    if count <= self.number_of_rectangles * 2:
                        faces_front2.append(count)
                        count += 2
                    else:
                        pass

        return self

    def SpeckleMeshByCone(self, verts, faces):
        spcklmesh = SpeckleMesh(vertices=verts, faces=faces, name="Joas", units="mm")
        return spcklmesh

    def SpeckleOb(self):
        self.SpeckleObjUp = [self.SpeckleMeshByCone(self.vertices_up, self.faces_up)]
        self.SpeckleObjUp2 = [self.SpeckleMeshByCone(self.vertices2, self.faces2)]

        self.SpeckleObjRight = [self.SpeckleMeshByCone(self.vertices_right, self.faces_right)]
        self.SpeckleObjRight2 = [self.SpeckleMeshByCone(self.vertices_right2, self.faces_right2)]

        self.SpeckleObjFront = [self.SpeckleMeshByCone(self.vertices_front, self.faces_front)]
        self.SpeckleObjFront2 = [self.SpeckleMeshByCone(self.vertices_front2, self.faces_front2)]
    #
        self.lst = [self.SpeckleObjUp, self.SpeckleObjUp2, self.SpeckleObjRight, self.SpeckleObjRight2, self.SpeckleObjFront, self.SpeckleObjFront2]
        return self

    # Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", lst, "Shiny Commit")
