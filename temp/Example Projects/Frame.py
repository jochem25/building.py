from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *
from project import fileformat
from objects.datum import *
from geometry.systemsimple import *

project = BuildingPy("Project Aanbouw","0")

Beam1 = Frame.byStartpointEndpointProfileName(Point(0,0,0),Point(3000,0,0),"HEA200","HEA200",BaseSteel)

project.objects.append(Beam1)

project.toSpeckle("f66b54f6c4")