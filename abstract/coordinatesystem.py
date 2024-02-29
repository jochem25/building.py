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


"""This module provides tools for coordinatesystems
"""

from geometry.point import Point
from abstract.vector import *
from pathlib import Path
import sys
import os
import math
__title__ = "coordinatesystem"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/coordinatesystem.py"


sys.path.append(str(Path(__file__).resolve().parents[1]))

# from project.fileformat import project

# [!not included in BP singlefile - end]


class CoordinateSystem:
    # UNITY VECTORS REQUIRED #TOdo organize resic
    def __init__(self, origin: Point, xaxis, yaxis, zaxis):
        self.id = generateID()
        self.type = __class__.__name__
        self.Origin = origin
        self.Xaxis = Vector3.normalize(xaxis)
        self.Yaxis = Vector3.normalize(yaxis)
        self.Zaxis = Vector3.normalize(zaxis)

    def serialize(self):
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'Origin': self.Origin.serialize(),
            'Xaxis': self.Xaxis.serialize(),
            'Yaxis': self.Yaxis.serialize(),
            'Zaxis': self.Zaxis.serialize()
        }

    @staticmethod
    def deserialize(data):
        origin = Point.deserialize(data['Origin'])
        xaxis = Vector3.deserialize(data['Xaxis'])
        yaxis = Vector3.deserialize(data['Yaxis'])
        zaxis = Vector3.deserialize(data['Zaxis'])
        return CoordinateSystem(origin, xaxis, yaxis, zaxis)

    # @classmethod
    # def by_origin(self, origin: Point):
    #     self.Origin = origin
    #     self.Xaxis = XAxis
    #     self.Yaxis = YAxis
    #     self.Zaxis = ZAxis
    #     return self

    @classmethod
    def by_origin(self, origin: Point):
        from abstract.coordinatesystem import XAxis, YAxis, ZAxis
        return self(origin, xaxis=XAxis, yaxis=YAxis, zaxis=ZAxis)

    # @staticmethod
    # def translate(CSOld, direction):
    #     CSNew = CoordinateSystem(CSOld.Origin, CSOld.Xaxis, CSOld.Yaxis, CSOld.Zaxis)
    #     new_origin = Point.translate(CSNew.Origin, direction)
    #     CSNew.Origin = new_origin
    #     return CSNew

    @staticmethod
    def translate(CSOld, direction: Vector3):
        from abstract.vector import Vector3
        pt = CSOld.Origin
        new_origin = Point.translate(pt, direction)

        XAxis = Vector3(1, 0, 0)

        YAxis = Vector3(0, 1, 0)

        ZAxis = Vector3(0, 0, 1)

        CSNew = CoordinateSystem(
            new_origin, xaxis=XAxis, yaxis=YAxis, zaxis=ZAxis)

        CSNew.Origin = new_origin
        return CSNew


    @staticmethod
    def transform(CS1, CS2): #incorrect output
        """
        Transforms CS1 into the coordinate system defined by CS2.
        :param CS1: The original CoordinateSystem instance.
        :param CS2: The target CoordinateSystem instance.
        :return: A new CoordinateSystem instance aligned with CS2.
        """
        from abstract.vector import Vector3
        import numpy as np

        translation_vector = Vector3.subtract(CS2.Origin, CS1.Origin)

        rotation_matrix = CoordinateSystem.calculate_rotation_matrix(
            CS1.Xaxis, CS1.Yaxis, CS1.Zaxis, CS2.Xaxis, CS2.Yaxis, CS2.Zaxis)

        xaxis_transformed = np.dot(rotation_matrix, Vector3.to_matrix(CS1.Xaxis))
        yaxis_transformed = np.dot(rotation_matrix, Vector3.to_matrix(CS1.Yaxis))
        zaxis_transformed = np.dot(rotation_matrix, Vector3.to_matrix(CS1.Zaxis))

        xaxis_normalized = Vector3.normalize(Vector3.from_matrix(xaxis_transformed))
        yaxis_normalized = Vector3.normalize(Vector3.from_matrix(yaxis_transformed))
        zaxis_normalized = Vector3.normalize(Vector3.from_matrix(zaxis_transformed))

        new_origin = Point.translate(CS1.Origin, translation_vector)
        new_CS = CoordinateSystem(new_origin, xaxis_normalized, yaxis_normalized, zaxis_normalized)

        return new_CS


    @staticmethod
    def translate_origin(origin1: Point, origin2: Point):

        origin1_np = np.array([origin1.x, origin1.y, origin1.z])
        origin2_np = np.array([origin2.x, origin2.y, origin2.z])

        new_origin_np = origin1_np + (origin2_np - origin1_np)
        return Point(new_origin_np[0], new_origin_np[1], new_origin_np[2])

    @staticmethod
    def calculate_rotation_matrix(xaxis1: Vector3, yaxis1: Vector3, zaxis1: Vector3, xaxis2: Vector3, yaxis2: Vector3, zaxis2: Vector3):
        from abstract.vector import Vector3

        R1 = np.array([Vector3.to_matrix(xaxis1), Vector3.to_matrix(
            yaxis1), Vector3.to_matrix(zaxis1)]).T
        R2 = np.array([Vector3.to_matrix(xaxis2), Vector3.to_matrix(
            yaxis2), Vector3.to_matrix(zaxis2)]).T

        rotation_matrix = np.dot(R2, np.linalg.inv(R1))
        return rotation_matrix

    @staticmethod
    def normalize(self):
        """
        Normalizes the axes of the coordinate system to make them unit vectors.
        """
        self.Xaxis = Vector3.normalize(self.Xaxis)
        self.Yaxis = Vector3.normalize(self.Yaxis)
        self.Zaxis = Vector3.normalize(self.Zaxis)

    #     norm = np.linalg.norm(v)
    #     return v / norm if norm > 0 else v



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
    def by_point_main_vector(self, NewOriginCoordinateSystem: Point, DirectionVectorZ: Vector3):
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

    def __str__(self):
        return f"{__class__.__name__}(Origin = " + f"{self.Origin}, XAxis = {self.Xaxis}, YAxis = {self.Yaxis}, ZAxis = {self.Zaxis})"


XAxis = Vector3(1, 0, 0)
Vector3(0, 1, 0)
Vector3(0, 0, 1)
CSGlobal = CoordinateSystem(Point(0, 0, 0), XAxis, YAxis, ZAxis)
