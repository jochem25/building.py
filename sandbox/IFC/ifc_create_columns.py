import ifcopenshell
from ifcopenshell.api import run
import ifcopenshell.util.placement
import numpy as np
import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from geometry.point import *
from abstract.vector import *


model = ifcopenshell.file()

project = run("root.create_entity", model, ifc_class="IfcProject", name="My Project")

run("unit.assign_unit", model)

context = run("context.add_context", model, context_type="Model")

body = run("context.add_context", model, context_type="Model",
    context_identifier="Body", target_view="MODEL_VIEW", parent=context)

site = run("root.create_entity", model, ifc_class="IfcSite", name="My Site")
building = run("root.create_entity", model, ifc_class="IfcBuilding", name="Building A")
storey = run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Ground Floor")

run("aggregate.assign_object", model, relating_object=project, product=site)
run("aggregate.assign_object", model, relating_object=site, product=building)
run("aggregate.assign_object", model, relating_object=building, product=storey)


def place_structural_element(model, from_point:Point, to_point:Point, element_type:str, profilename:str, materialname=None) -> object:
    ifc_class_type = "IfcColumnType" if element_type.lower() == "column" else "IfcBeamType"
    ifc_class = "IfcColumn" if element_type.lower() == "column" else "IfcBeam"

    targetY = from_point.y
    gunY = to_point.y

    targetX = from_point.x
    gunX = to_point.x

    numerator = gunY-targetY
    denominator = gunX-targetX

    atvalue_rad = math.atan2(numerator, denominator)
    atvalue_deg = math.degrees(atvalue_rad)

    distance = Point.distance(from_point, to_point)

    x_rad = math.atan2(distance, (to_point.z-from_point.z))
    print(x_rad)
    x_deg = math.degrees(x_rad)-90
    print(x_deg)
    

    column_type = run("root.create_entity", model, ifc_class=ifc_class_type, name="C2")
    matrix = np.eye(4)

    matrix = ifcopenshell.util.placement.rotation(90, "X") @ matrix
    matrix = ifcopenshell.util.placement.rotation(90, "Z") @ matrix
    # matrix = ifcopenshell.util.placement.rotation(0, "Y") @ matrix -> direction works

    matrix = ifcopenshell.util.placement.rotation(35, "Y") @ matrix
    matrix = ifcopenshell.util.placement.rotation(atvalue_deg, "Z") @ matrix

    matrix[:,3][0:3] = (P1[0], P1[1], P1[2])

    material_set = run("material.add_material_set", model, name="C2", set_type="IfcMaterialProfileSet")
    steel = run("material.add_material", model, name=materialname, category="steel")
    shape_profile = model.create_entity("IfcIShapeProfileDef", ProfileName=profilename, ProfileType="AREA", OverallWidth=100, OverallDepth=96, WebThickness=5, FlangeThickness=8, FilletRadius=12, )
    run("material.add_profile", model, profile_set=material_set, material=steel, profile=shape_profile)
    run("material.assign_material", model, product=column_type, material=material_set)
    column = run("root.create_entity", model, ifc_class=ifc_class)
    run("geometry.edit_object_placement", model, product=column, matrix=matrix, is_si=True)
    run("type.assign_type", model, related_object=column, relating_type=column_type)
    representation = run("geometry.add_profile_representation", model, context=body, profile=shape_profile, depth=distance)
    run("geometry.assign_representation", model, product=column, representation=representation)
    run("spatial.assign_container", model, relating_structure=storey, product=column)



#create beam
beam_type = run("root.create_entity", model, ifc_class="IfcBeamType", name="B1")
matrix = np.eye(4)
length = 2

P1 = [0,0,0]
P2 = [1,2,3]

# P1 = [43,1,-45]
# P2 = [8,23,12]

# P1 = [30,30,10]
# P2 = [1,23,113]

targetY = P1[1]
gunY = P2[1]

targetX = P1[0]
gunX = P2[0]

numerator = gunY-targetY
denominator = gunX-targetX

atvalue_rad = math.atan2(numerator, denominator)
atvalue_deg = math.degrees(atvalue_rad)

distance = Point.distance(Point.from_matrix(P1), Point.from_matrix(P2))
# print(distance)
matrix[:,3][0:3] = (P1[0], P1[1], P1[2])

XYdegree_rad = math.atan2(gunY, distance)
XYdegree_deg = math.degrees(atvalue_deg)
print(XYdegree_deg)

material_set = run("material.add_material_set", model, name="B1", set_type="IfcMaterialProfileSet")
steel = run("material.add_material", model, name="ST01", category="steel")
hea100 = model.create_entity("IfcIShapeProfileDef", ProfileName="HEA100", ProfileType="AREA", OverallWidth=100, OverallDepth=96, WebThickness=5, FlangeThickness=8, FilletRadius=12, )
run("material.add_profile", model, profile_set=material_set, material=steel, profile=hea100)
run("material.assign_material", model, product=beam_type, material=material_set)
beam = run("root.create_entity", model, ifc_class="IfcBeam")
run("geometry.edit_object_placement", model, product=beam, matrix=matrix, is_si=True)

run("type.assign_type", model, related_object=beam, relating_type=beam_type)
representation = run("geometry.add_profile_representation", model, context=body, profile=hea100, depth=length)
run("geometry.assign_representation", model, product=beam, representation=representation)
run("spatial.assign_container", model, relating_structure=storey, product=beam)


#create column
column_type = run("root.create_entity", model, ifc_class="IfcColumnType", name="C1")
matrix = np.eye(4)
matrix[:,3][0:3] = (P2[0], P2[1], P2[2])

material_set = run("material.add_material_set", model, name="C1", set_type="IfcMaterialProfileSet")
steel = run("material.add_material", model, name="ST01", category="steel")
hea100 = model.create_entity("IfcIShapeProfileDef", ProfileName="HEA120", ProfileType="AREA", OverallWidth=100, OverallDepth=96, WebThickness=5, FlangeThickness=8, FilletRadius=12, )
run("material.add_profile", model, profile_set=material_set, material=steel, profile=hea100)
run("material.assign_material", model, product=column_type, material=material_set)
column = run("root.create_entity", model, ifc_class="IfcColumn")
run("geometry.edit_object_placement", model, product=column, matrix=matrix, is_si=True)
run("type.assign_type", model, related_object=column, relating_type=column_type)
representation = run("geometry.add_profile_representation", model, context=body, profile=hea100, depth=length)
run("geometry.assign_representation", model, product=column, representation=representation)
run("spatial.assign_container", model, relating_structure=storey, product=column)


place_structural_element(model, Point.from_matrix(P1), Point.from_matrix(P2), "beam", "HEA120", "c33")


model.write("model1.ifc")