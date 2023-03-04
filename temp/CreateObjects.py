from objects.panel import *
from objects.frame import *
from objects.shape import *
from exchange.speckle import *

pan1 = Panel.byBaselineHeight(Line(start= Point(1000,0,0),end=Point(3000,0,0)),2500,150,"wand")
pan2 = Panel.byBaselineHeight(Line(start= Point(1000,0,0),end=Point(3000,0,0)),2500,150,"wand")

#sys.exit()
frame2 = Frame.byStartpointEndpointProfileName(Point(0,0,0), Point(0,1000,0), "UPE80", "test")

data = searchProfile("UNP80").shape_coords
data2 = profiledataToShape("UNP80")

print(data2)
#sys.exit()
frame3 = Frame.byStartpointEndpointProfileName(Point(500,0,0), Point(500,1000,0), "UNP100", "test")

SpeckleObj = translateObjectsToSpeckleObjects([frame2,frame3,pan1,pan2])

Commit = TransportToSpeckle("3bm.exchange", "9548edd190", SpeckleObj, "Shiny Commit")