import sys, os
from pathlib import Path
import json
from collections import defaultdict

sys.path.append(str(Path(__file__).resolve().parents[1]))

from objects.frame import *
from exchange.scia import *

from objects.analytical import *
from project.fileformat import BuildingPy

point = Point(1.0, 2.0, 3.0)
serialized_point1 = json.dumps(point.serialize())

p2 = Point(20, 3, 50)
serialized_point2 = json.dumps(p2.serialize())
line1 = Line(point, p2)

serialized_line1 = json.dumps(line1.serialize())



v2 = Vector3(20,10,30)
serialized_vect = json.dumps(v2.serialize())

serialized_objects = [serialized_point1, serialized_point2, serialized_vect]
serialized_data = json.dumps(serialized_objects)

file_name = 'project/data.json'
with open(file_name, 'w') as file:
    file.write(serialized_data)

# Extract and count unique types
type_count = defaultdict(int)
for serialized_item in serialized_objects:
    item = json.loads(serialized_item)
    item_type = item.get("type")
    if item_type:
        type_count[item_type] += 1

total_items = len(serialized_objects)

print(f"Total saved items to '{file_name}': {total_items}\n")
print("Type counts:")
for item_type, count in type_count.items():
    print(f"{item_type}: {count}")

# project.save(path)
# replace or merge at saving