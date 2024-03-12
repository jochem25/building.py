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


"""This module provides tools to create linestyles and patterns
"""

__title__ = "linestyle"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/linestyle.py"


import sys, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.vector import *
from geometry.curve import *


# [!not included in BP singlefile - end]

# Rule: line, whitespace, line whitespace etc., scale
HiddenLine1 = ["Hidden Line 1", [1, 1], 100]
# Rule: line, whitespace, line whitespace etc., scale
HiddenLine2 = ["Hidden Line 2", [2, 1], 100]
# Rule: line, whitespace, line whitespace etc., scale
Centerline = ["Center Line 1", [8, 2, 2, 2], 100]


def line_to_pattern(baseline, patternobj):
    # this converts a line to list of lines based on a pattern
    origin = baseline.start
    dir = Vector3.by_two_points(baseline.start, baseline.end)
    unityvect = Vector3.normalize(dir)

    Pattern = patternobj
    l = baseline.length
    patternlength = sum(Pattern[1]) * Pattern[2]
    # number of whole lengths of the pattern
    count = math.floor(l / patternlength)
    lines = []

    startpoint = origin
    ll = 0
    rl = 10000
    for i in range(count + 1):
        n = 0
        for i in Pattern[1]:
            deltaV = Vector3.product(i * Pattern[2], unityvect)
            dl = Vector3.length(deltaV)
            if rl < dl:  # this is the last line segment on the line where the pattern is going to be cut into pieces.
                endpoint = baseline.end
            else:
                endpoint = Point.translate(startpoint, deltaV)
            if n % 2:
                a = 1 + 1
            else:
                lines.append(Line(start=startpoint, end=endpoint))
            if rl < dl:
                break  # end of line reached
            startpoint = endpoint
            n = n + 1
            ll = ll + dl  # total length
            rl = l - ll  # remaining length within the pattern
        startpoint = startpoint
    return lines
