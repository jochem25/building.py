# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij                              *
# *   maarten@3bm.co.nl                                                     *
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


"""This module provides tools to create solids
"""

__title__ = "mesh"
__author__ = "Maarten"
__url__ = "./geometry/solid.py"


class MeshPB:
    """Represents a mesh object with vertices, faces, and other attributes."""
    def __init__(self):
        """The MeshPB class is designed to construct mesh objects from vertices and faces. It supports creating meshes from a variety of inputs including vertex-face lists, polycurves, and coordinate lists with support for nested structures.
        
        - `verts` (list): A list of vertices that make up the mesh.
        - `faces` (list): A list defining the faces of the mesh. Each face is represented by indices into the `verts` list.
        - `numberFaces` (int): The number of faces in the mesh.
        - `name` (str): The name of the mesh.
        - `material` (Material): The material assigned to the mesh.
        - `colorlst` (list): A list of colors for the mesh, derived from the material.
        """
        self.type = __class__.__name__
        self.verts = []
        self.faces = []
        self.numberFaces = 0
        self.name = None
        self.material = None
        self.colorlst = []

    def by_verts_faces(self, verts: 'list', faces: 'list') -> 'MeshPB':
        """Initializes the mesh with vertices and faces.

        #### Parameters:
        - `verts` (list): A list of vertices.
        - `faces` (list): A list of faces. Each face is a list of indices into the `verts` list.

        This method directly sets the vertices and faces of the mesh based on the input lists.
        
        #### Example usage:
        ```python

        ```
        """
        self.verts = verts
        self.faces = faces

    #create material class; Material
    def by_polycurve(self, PC, name: 'str', material) -> 'MeshPB':
        """Creates a mesh from a polycurve object.

        #### Parameters:
        - `PC` (Polycurve): A polycurve object from which to generate the mesh.
        - `name` (str): The name of the mesh.
        - `material` (Material): The material to apply to the mesh.

        This method constructs the mesh such that it represents the shape defined by the polycurve.
        
        #### Example usage:
        ```python

        ```
        """
        # Mesh of single face
        verts = []
        faces = []
        # numberFaces = 0
        n = 0  # number of vert. Every vert has a unique number in the list
        pnts = PC.points  # points in every polycurve
        faces.append(len(pnts))  # number of verts in face
        for j in pnts:
            faces.append(n)
            verts.append(j.x)
            verts.append(j.y)
            verts.append(j.z)
            n = n + 1
        self.verts = verts
        self.faces = faces
        # ex.numberFaces = numberFaces
        self.name = name
        self.material = material
        self.colorlst = [material.colorint]
        return self

    def by_coords(self, lsts: 'list', name: 'str', material, doublenest: 'bool') -> 'MeshPB':
        """Creates a mesh from a list of coordinates.

        #### Parameters:
        - `lsts` (list): A nested list of coordinates defining the vertices of the mesh.
        - `name` (str): The name of the mesh.
        - `material` (Material): The material to apply to the mesh.
        - `doublenest` (bool): A flag indicating if the list of coordinates is double-nested.

        This method allows for flexible mesh creation from complex nested list structures of coordinates.
        
        #### Example usage:
        ```python

        ```
        """
        # Example list structure, can be multiple as wel
        # [[[[8252, 2129, 1520], [-6735, 1188, 1520], [8753, -5855, 1520]]], [[[-6735, 1188, 1520], [-6234, -6796, 1520], [8753, -5855, 1520]]], [[[8252, 2129, 870], [8753, -5855, 1520], [8753, -5855, 870]]], [[[8252, 2129, 870], [8252, 2129, 1520], [8753, -5855, 1520]]], [[[8753, -5855, 870], [-6234, -6796, 1520], [-6234, -6796, 870]]], [[[8753, -5855, 870], [8753, -5855, 1520], [-6234, -6796, 1520]]], [[[-6234, -6796, 870], [-6735, 1188, 1520], [-6735, 1188, 870]]], [[[-6234, -6796, 870], [-6234, -6796, 1520], [-6735, 1188, 1520]]], [[[-6735, 1188, 870], [8252, 2129, 1520], [8252, 2129, 870]]], [[[-6735, 1188, 870], [-6735, 1188, 1520], [8252, 2129, 1520]]], [[[-6735, 1188, 870], [8252, 2129, 870], [8753, -5855, 870]]], [[[-6234, -6796, 870], [-6735, 1188, 870], [8753, -5855, 870]]]]
        verts = []
        faces = []
        count = 0
        # lst is [[8252, 2129, 1520], [-6735, 1188, 1520], [8753, -5855, 1520]]
        for lst in lsts:
            if doublenest:
                # lst is [8252, 2129, 1520], [-6735, 1188, 1520], [8753, -5855, 1520], [8753, -5855, 1520]
                lst = lst[0]
            else:
                lst = lst
            faces.append(len(lst))
            for coord in lst:  # [8252, 2129, 1520]
                faces.append(count)
                verts.append(coord[0])  # x
                verts.append(coord[1])  # y
                verts.append(coord[2])  # z
                count += 1
            self.numberFaces = + 1
        for j in range(int(len(verts) / 3)):
            self.colorlst.append(material.colorint)
        self.verts = verts
        self.faces = faces
        self.name = name
        self.material = material
        return self
