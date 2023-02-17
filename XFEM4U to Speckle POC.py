#from . import Struct4U
#from geometry.point import Point
#from geometry.curve import Line

import xml.etree.ElementTree as ET
import sys

tree = ET.parse("C:/TEMP/test135.xml")
# get data from xml
root = tree.getroot()

#SPECKLE PART

from specklepy.objects.geometry import Point
from specklepy.objects.geometry import Line
from specklepy.objects.geometry import Polyline
from exchange.speckle import *
from geometry.point import Point
from objects.frame import Frame
from exchange.XFEM4U.xfem4unames import *

def getGridDistances(Grids):
    del Grids[0]
    GridsNew = []
    distance = 0.0
    for i in Grids:
        if "x" in i:
            spl = i.split("x")
            count = int(spl[0])
            width = float(spl[1])
            for i in range(count):
                GridsNew.append(distance)
                distance = distance + width
        else:
            GridsNew.append(distance)
            distance = distance + float(i)
    return GridsNew

#List for SpeckleObjects
obj = []

#GRIDS
GridEx = 1000

GridsX = root.findall(".//Grids/X")[0].text.split()
GridsX = getGridDistances(GridsX)
Xmax = max(GridsX)
GridsXLable = root.findall(".//Grids/X_Lable")[0].text.split()
GridsY = root.findall(".//Grids/Y")[0].text.split()
GridsY = getGridDistances(GridsY)
Ymax = max(GridsY)
GridsYLable = root.findall(".//Grids/Y_Lable")[0].text.split()
GridsZ = root.findall(".//Grids/Z")[0].text.split()
GridsZ = getGridDistances(GridsZ)
GridsZLable = root.findall(".//Grids/Z_Lable")[0].text.split()
Zmax = max(GridsZ)

from geometry.curve import *

grids = []
for i in GridsX:
    grids.append(Line(Point(i,-GridEx,0),Point(i,Ymax+GridEx,0)))

for i in GridsY:
    grids.append(Line(Point(i,-GridEx,0),Point(i,Ymax+GridEx,0)))

for i in GridsZ:
    grids.append(Line(Point(i,-GridEx,0),Point(i,Ymax+GridEx,0)))

for i in grids:
    line = LineToSpeckleLine(i) #Grid naar SpeckleLine
    obj.append(line)

#PUNTEN IMPORTEREN
n = root.findall(".//Nodes/Number")
X = root.findall(".//Nodes/X")
Y = root.findall(".//Nodes/Y")
Z = root.findall(".//Nodes/Z")

XYZ = []

#Punten in 3D in Speckle tekenen
for h,i,j,k in zip(n,X,Y,Z):
    Pnt = Point(float(i.text), float(j.text), float(k.text))
    #Pnt.id = int(h.text)
    XYZ.append(Pnt)

#BEAMS
BeamsFrom = root.findall(".//Beams/From_node_number")
BeamsNumber = root.findall(".//Beams/Number")
BeamsTo = root.findall(".//Beams/To_node_number")
BeamsName = root.findall(".//Beams/Profile_number")

#PROFILES
ProfileNumber = root.findall(".//Profiles/Number")
ProfileName = root.findall(".//Profiles/Profile_name")


for i, j, k, l in zip(BeamsFrom, BeamsTo, BeamsName, BeamsNumber):
    profile_name = ProfileName[int(k.text)-1].text
    if profile_name == None:
        pass
    else:
        frame = Frame()
        start = XYZ[int(i.text)-1]
        end = XYZ[int(j.text)-1]
        profile = matchprofile(profile_name)
        try:
            frame.byStartpointEndpointProfileName(start, end, profile, profile_name + "-" + l.text)
        except:
            pass
        test = SpeckleMeshByMesh(frame)
        obj.append(test)

#PLATES

PlatesNumber = root.findall(".//Plates/Number")
PlatesNodes = root.findall(".//Plates/Node")

PlatePoints = []
# for loop to get each element in an array

rootPlates = root.findall(".//Plates")

XMLelements = []
for elem in rootPlates:
    XMLelements.append(elem.text)

print(XMLelements)

#HOE NODES TE GROEPEREN

for i in PlatesNodes:
    PlatePoints.append(XYZ[int(i.text)-1])

#plyline = Polyline.from_points(PlatePoints)

#sys.exit()

SpeckleHost = "speckle.xyz"
StreamID = "a2ff034164"
SpeckleObjects = obj
Message = "I send this to Speckle on 14-02-2023"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)

print(Commit)
