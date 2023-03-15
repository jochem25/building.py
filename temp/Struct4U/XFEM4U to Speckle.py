from exchange.struct4U import *
from exchange.speckle import *
from abstract.plane import *
from objects.panel import *
from objects.frame import *
import xml.etree.ElementTree as ET

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

#tree = ET.parse("/temp/testplates.xml")
tree = ET.parse("C:/Users/mikev/3BM Dropbox/Maarten Vroegindeweij/Struct4U/Example Projects/Industrial steel structure 2/export.xml")
root = tree.getroot()


#TODO: Lines and Grids units
#TODO: Beams in node
#TODO: Materialcolor
#TODO: Concrete Profiles

#LoadGrid and create in Speckle
Grids = XMLImportGrids(tree,1000)
XYZ = XMLImportNodes(tree)
obj = XMLImportPlates(tree)

#GridSystem()
print(profiledataToShape("S80X10"))
print(profiledataToShape("HFRHS250X250X10"))
print(profiledataToShape("L70X70X6"))
print(profiledataToShape("HFRHS80X80X5"))


Frame.byStartpointEndpointProfileName(Point(0,0,0), Point(1000,0,0), "S80X10", "S80X10")
Frame.byStartpointEndpointProfileName(Point(0,0,0), Point(1000,0,0), "HFRHS250X250X10", "HFRHS250X250X10")
Frame.byStartpointEndpointProfileName(Point(0,0,0), Point(1000,0,0), "L70X70X6", "L70X70X6")
Frame.byStartpointEndpointProfileName(Point(0,0,0), Point(1000,0,0), "HFRHS80X80X5", "HFRHS80X80X5")


print(Grids)
sys.exit()
#BEAMS
BeamsFrom = root.findall(".//Beams/From_node_number")
BeamsNumber = root.findall(".//Beams/Number")
BeamsTo = root.findall(".//Beams/To_node_number")
BeamsName = root.findall(".//Beams/Profile_number")

#print(BeamsFrom)
#PROFILES
ProfileNumber = root.findall(".//Profiles/Number")
ProfileNumber = root.findall(".//Profiles/Material_type")
ProfileName = root.findall(".//Profiles/Profile_name")

#sys.exit()

beams = []
for i, j, k, l in zip(BeamsFrom, BeamsTo, BeamsName, BeamsNumber):
    profile_name = ProfileName[int(k.text)-1].text
    if profile_name == None:
        pass
    else:
        start = XYZ[1][XYZ[0].index(i.text)]
        end = XYZ[1][XYZ[0].index(j.text)]
        try:
            obj.append(Frame.byStartpointEndpointProfileName(start, end, profile_name, profile_name + "-" + l.text))
        except:
            pass
            print("could not translate " + profile_name)

SpeckleObj = translateObjectsToSpeckleObjects(obj)

print(profiledataToShape("S80X10"))
print(profiledataToShape("HFRHS250X250X10"))
print(profiledataToShape("L70X70X6"))
print(profiledataToShape("HFRHS80X80X5"))

#sys.exit()

Commit = TransportToSpeckle("struct4u.xyz", "61c1210d76", SpeckleObj, "Test with Plates from XFEM4U")