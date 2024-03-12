# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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


"""This module provides tools to create points
"""

from abstract import vector
from helper import *
from pathlib import Path
__title__ = "point"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/point.py"


import sys
import math
# from abstract.coordinatesystem import *
file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

# [!not included in BP singlefile - end]

# from project.fileformat import project


class Point:
    def __init__(self, x, y, z):
        self.id = generateID()
        self.type = __class__.__name__
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.value = self.x, self.y, self.z
        self.units = "mm"

    def __str__(self) -> str:
        return f"{__class__.__name__}(X = {self.x:.3f}, Y = {self.y:.3f}, Z = {self.z:.3f})"

    def serialize(self):
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'value': self.value,
            'units': self.units
        }

    @staticmethod
    def deserialize(data):
        return Point(data['x'], data['y'], data['z'])

    @staticmethod
    def distance(point1, point2):
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)

    @staticmethod
    def calculate_distance(points: list) -> float:
        distances = []
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                distances.append(
                    (points[i], points[j], Point.distance(points[i], points[j])))
        distances.sort(key=lambda x: x[2])
        return distances

    @staticmethod
    def difference(pointxyz1, pointxyz2):
        from abstract.vector import Vector3
        return Vector3(
            pointxyz2.x - pointxyz1.x,
            pointxyz2.y - pointxyz1.y,
            pointxyz2.z - pointxyz1.z
        )

    @staticmethod
    def translate(point, vector):
        from abstract.vector import Vector3

        ar1 = Point.to_matrix(point)
        ar2 = Vector3.to_matrix(vector)
        if len(ar1) == len(ar2):
            c = [ar1[i] + ar2[i] for i in range(len(ar1))]
        else:
            c = [0, 0, 0]
            raise ValueError("Arrays must have the same size")
        return Point(c[0], c[1], c[2])

    @staticmethod
    def origin(point1, point2):
        return Point(
            (point1.x + point2.x) / 2,
            (point1.y + point2.y) / 2,
            (point1.z + point2.z) / 2
        )

    @staticmethod
    def point_2D_to_3D(point2D):
        return Point(
            point2D.x,
            point2D.y,
            0
        )

    @staticmethod
    def to_vector(point1):
        from abstract.vector import Vector3
        return Vector3(
            point1.x,
            point1.y,
            point1.z
        )

    @staticmethod
    def sum(p1, p2):
        return Point(
            p1.x + p2.x,
            p1.y + p2.y,
            p1.z + p2.z
        )

    @staticmethod
    def diff(p1, p2):
        return Point(
            p1.x - p2.x,
            p1.y - p2.y,
            p1.z - p2.z
        )

    @staticmethod
    def rotate_XY(p1, Beta, dz):
        return Point(
            math.cos(math.radians(Beta))*p1.x -
            math.sin(math.radians(Beta))*p1.y,
            math.sin(math.radians(Beta))*p1.x +
            math.cos(math.radians(Beta))*p1.y,
            p1.z + dz
        )

    def product(n, p1):  # Same as scale
        return Point(
            p1.x*n,
            p1.y*n,
            p1.z*n
        )

    @staticmethod
    def intersect(p1, p2):
        # Intersection of two points
        if p1.x == p2.x and p1.y == p2.y and p1.z == p2.z:
            return 1
        else:
            return 0

    @staticmethod
    def to_matrix(self):
        return [self.x, self.y, self.z]

    @staticmethod
    def from_matrix(self):
        return Point(
            self[0],
            self[1],
            self[2]
        )


class CoordinateSystem:
    # UNITY VECTORS REQUIRED
    def __init__(self, origin: Point, xaxis, yaxis, zaxis):
        from abstract.vector import Vector3
        self.id = generateID()
        self.type = __class__.__name__
        self.Origin = origin
        self.Xaxis = Vector3.normalize(xaxis)
        self.Yaxis = Vector3.normalize(yaxis)
        self.Zaxis = Vector3.normalize(zaxis)

    @classmethod
    def by_origin(self, origin: Point):
        from abstract.coordinatesystem import XAxis, YAxis, ZAxis
        return self(origin, xaxis=XAxis, yaxis=YAxis, zaxis=ZAxis)

    @staticmethod
    def translate(CSOld, direction):
        from abstract.vector import Vector3
        new_origin = Point.translate(CSOld.Origin, direction)

        XAxis = Vector3(1, 0, 0)

        YAxis = Vector3(0, 1, 0)

        ZAxis = Vector3(0, 0, 1)

        CSNew = CoordinateSystem(
            new_origin, xaxis=XAxis, yaxis=YAxis, zaxis=ZAxis)

        CSNew.Origin = new_origin
        return CSNew

    def __str__(self):
        return f"{__class__.__name__}(Origin = " + f"{self.Origin}, XAxis = {self.Xaxis}, YAxis = {self.Yaxis}, ZAxis = {self.Zaxis})"

    @staticmethod
    def by_point_main_vector(self, NewOriginCoordinateSystem: Point, DirectionVectorZ):
        from abstract.vector import Vector3
        vz = DirectionVectorZ  # LineVector and new Z-axis
        vz = Vector3.normalize(vz)  # NewZAxis
        vx = Vector3.perpendicular(vz)[0]  # NewXAxis
        try:
            vx = Vector3.normalize(vx)  # NewXAxisnormalized
        except:
            # In case of vertical element the length is zero
            vx = Vector3(1, 0, 0)
        vy = Vector3.perpendicular(vz)[1]  # NewYAxis
        try:
            vy = Vector3.normalize(vy)  # NewYAxisnormalized
        except:
            # In case of vertical element the length is zero
            vy = Vector3(0, 1, 0)
        CSNew = CoordinateSystem(NewOriginCoordinateSystem, vx, vy, vz)
        return CSNew

    @staticmethod
    def move_local(CSOld, x: float, y: float, z: float):
        from abstract.vector import Vector3
        # move coordinatesystem by y in local coordinates(not global)
        xloc_vect_norm = CSOld.Xaxis
        xdisp = Vector3.scale(xloc_vect_norm, x)
        yloc_vect_norm = CSOld.Xaxis
        ydisp = Vector3.scale(yloc_vect_norm, y)
        zloc_vect_norm = CSOld.Xaxis
        zdisp = Vector3.scale(zloc_vect_norm, z)
        disp = Vector3.sum3(xdisp, ydisp, zdisp)
        CS = CoordinateSystem.translate(CSOld, disp)
        return CS

    @staticmethod
    def translate_origin(origin1, origin2):

        origin1_n = Point.to_matrix(origin1)
        origin2_n = Point.to_matrix(origin2)

        new_origin_n = origin1_n + (origin2_n - origin1_n)
        return Point(new_origin_n[0], new_origin_n[1], new_origin_n[2])

    @staticmethod
    def calculate_rotation_matrix(xaxis_1, yaxis_1, zaxis_1, xaxis_2, yaxis_2, zaxis_2):
        from abstract.vector import Vector3

        R1 = [Vector3.to_matrix(xaxis_1), Vector3.to_matrix(
            yaxis_1), Vector3.to_matrix(zaxis_1)]

        R2 = [Vector3.to_matrix(xaxis_2), Vector3.to_matrix(
            yaxis_2), Vector3.to_matrix(zaxis_2)]

        R1_transposed = list(map(list, zip(*R1)))
        R2_transposed = list(map(list, zip(*R2)))

        rotation_matrix = Vector3.dot_product(Vector3.from_matrix(
            R2_transposed), Vector3.length(Vector3.from_matrix(R1_transposed)))
        return rotation_matrix

    @staticmethod
    def normalize(v):
        norm = (v[0]**2 + v[1]**2 + v[2]**2)**0.5
        return [v[0] / norm, v[1] / norm, v[2] / norm] if norm > 0 else v


def transform_point(point_local, coordinate_system_old, new_origin, direction_vector):
    from abstract.vector import Vector3

    direction_vector = Vector3.to_matrix(direction_vector)
    new_origin = Point.to_matrix(new_origin)
    vz_norm = Vector3.length(Vector3(*direction_vector))
    vz = [direction_vector[0] / vz_norm, direction_vector[1] /
          vz_norm, direction_vector[2] / vz_norm]

    vx = [-vz[1], vz[0], 0]
    vx_norm = Vector3.length(Vector3(*vx))

    if vx_norm == 0:
        vx = [1, 0, 0]
    else:
        vx = [vx[0] / vx_norm, vx[1] / vx_norm, vx[2] / vx_norm]

    vy = Vector3.cross_product(Vector3(*vz), Vector3(*vx))
    vy_norm = Vector3.length(vy)
    if vy_norm != 0:
        vy = [vy.x / vy_norm, vy.y / vy_norm, vy.z / vy_norm]
    else:
        vy = [0, 1, 0]

    P1 = point_local
    CSNew = CoordinateSystem(Point.from_matrix(new_origin), Vector3.from_matrix(
        vx), Vector3.from_matrix(vy), Vector3.from_matrix(vz))
    v1 = Point.difference(coordinate_system_old.Origin, CSNew.Origin)

    v2 = Vector3.product(P1.x, CSNew.Xaxis)
    v3 = Vector3.product(P1.y, CSNew.Yaxis)
    v4 = Vector3.product(P1.z, CSNew.Zaxis)
    vtot = Vector3(v1.x + v2.x + v3.x + v4.x, v1.y + v2.y +
                   v3.y + v4.y, v1.z + v2.z + v3.z + v4.z)
    pointNew = Point.translate(Point(0, 0, 0), vtot)

    return pointNew


def transform_point_2(PointLocal: Point, CoordinateSystemNew: CoordinateSystem):
    from abstract.vector import Vector3
    pn = Point.translate(CoordinateSystemNew.Origin, Vector3.scale(
        CoordinateSystemNew.Xaxis, PointLocal.x))
    pn2 = Point.translate(pn, Vector3.scale(
        CoordinateSystemNew.Yaxis, PointLocal.y))
    pn3 = Point.translate(pn2, Vector3.scale(
        CoordinateSystemNew.Zaxis, PointLocal.z))
    return pn3