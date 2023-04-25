from objects.frame import *
from exchange.speckle import *
from objects.datum import *
from objects.frame import *
from helpers import helper
#Proof of Concept modules

# GridSystem
nx = 5
ny = 5
spacing = 2950
heigth = 3300

spacX = str(nx) + "x" + str(spacing)  #"13x5400"
spacY = str(ny) + "x" + str(spacing)  #"4x5400"
grids = GridSystem(spacX,seqChar,spacY,seqNumber,2500)
obj = grids[0] + grids[1]

width = spacing
length = spacing *2

def flatten(lst):
    flat_list = []
    for sub in lst:
        try:
            for item in sub:
                flat_list.append(item)
        except:
            flat_list.append(sub) #This is not a list but an item
    return flat_list
def module(widthMod: float,lengthMod: float, heightMod: float,vector: Vector3,rot: bool, floorframing :bool):
    x = vector.X
    y = vector.Y
    z = vector.Z
    StartPoint = Point(x,y,z)

    if rot:
        length = widthMod
        width = lengthMod
    else:
        length = lengthMod
        width = widthMod
    Vdx = Vector3(length,0,0)
    Vdy = Vector3(0,width,0)
    Vdz = Vector3(0,0,heightMod)

    #Bottom
    P1 = StartPoint #Left Bottom
    P2 = Point.translate(StartPoint,Vdx) #Right Bottom
    P3 = Point.translate(P2,Vdy) #Right Top
    P4 = Point.translate(StartPoint,Vdy) #Left Top
    #Top
    P5 = Point.translate(P1,Vdz) #Left Bottom
    P6 = Point.translate(P2,Vdz) #Right Bottom
    P7 = Point.translate(P3,Vdz) #Right Top
    P8 = Point.translate(P4,Vdz) #Left Top

    obj = []
    #Bottom Frame
    obj.append(Frame.byStartpointEndpointProfileNameJustifiction(P2,P1,"UNP200","Frame","Left","bottom",0,BaseSteel))
    obj.append(Frame.byStartpointEndpointProfileNameJustifiction(P3,P2,"UNP200","Frame","Left","bottom",0,BaseSteel))
    obj.append(Frame.byStartpointEndpointProfileNameJustifiction(P4,P3,"UNP200","Frame","Left","bottom",0,BaseSteel))
    obj.append(Frame.byStartpointEndpointProfileNameJustifiction(P1,P4,"UNP200","Frame","Left","bottom",0,BaseSteel))

    #Bottom Floor Framing
    if floorframing:
        v1 = Vector3(610, 0, 0)
        count = int(math.floor(length/610))
        pb1 = P1
        pb2 = P4
        for i in range(count):
            pb1 = Point.translate(pb1,v1)
            pb2 = Point.translate(pb2,v1)
            obj.append(Frame.byStartpointEndpoint(pb1, pb2, Rectangle("71x196",71,196).curve.translate(Vector2(0,100)),"balk",0,BaseTimber))
    else:
        v1 = "skip"

    #Top Frame
    obj.append(Frame.byStartpointEndpointProfileNameJustifiction(P6,P5,"UNP200","Frame","Left","top",0,BaseSteel))
    obj.append(Frame.byStartpointEndpointProfileNameJustifiction(P7,P6,"UNP200","Frame","Left","top",0,BaseSteel))
    obj.append(Frame.byStartpointEndpointProfileNameJustifiction(P8,P7,"UNP200","Frame","Left","top",0,BaseSteel))
    obj.append(Frame.byStartpointEndpointProfileNameJustifiction(P5,P8,"UNP200","Frame","Left","top",0,BaseSteel))

    #Columns
    obj.append(Frame.byStartpointEndpointProfileNameShapevector(P1,P5,"K100/5","Column",Vector2(50,50),0,BaseSteel))
    obj.append(Frame.byStartpointEndpointProfileNameShapevector(P2,P6,"K100/5","Column",Vector2(-50,50),0,BaseSteel))
    obj.append(Frame.byStartpointEndpointProfileNameShapevector(P3,P7,"K100/5","Column",Vector2(-50,-50),0,BaseSteel))
    obj.append(Frame.byStartpointEndpointProfileNameShapevector(P4,P8,"K100/5","Column",Vector2(50,-50),0,BaseSteel))

    return obj

Modules = [ #Syntax: Level, GridX, GridY, Rotation # 0 is 0, 1 = 90
[0,0,0,0],
[0,0,1,0],
[0,0,2,0],
[0,0,3,0],
[0,0,4,0],
[0,2,1,1],
[0,2,3,1],
[0,3,1,0],
[0,3,2,0],
[0,3,3,0],
[0,3,4,0],

[2,0,0,0],
[2,0,1,0],
[2,0,2,0],
[2,0,3,0],
[2,0,4,0],
[2,2,1,1],
[2,2,3,1],
[2,3,1,0],
[2,3,2,0],
[2,3,3,0],
[2,3,4,0],
]

for i in Modules:
    V = Vector3(i[1]*spacing, i[2]*spacing,i[0]*heigth)
    if i[3] == 0:
        rot = 0
    elif i[3] == 1:
        rot = 90
    else:
        rot = 0
    obj.append(module(width, length, heigth, V, rot,1 ))

obj1 = flatten(obj)
SpeckleObj = translateObjectsToSpeckleObjects(obj1)
Commit = TransportToSpeckle("3bm.exchange", "17f6dbaddc", SpeckleObj, "Modules")

