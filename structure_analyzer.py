import xml.etree.ElementTree as ET
from collections import Counter

kml_file = "file.kml"

# Parse XML
tree = ET.parse(kml_file)
root = tree.getroot()

print("\n=========== GENERAL INFORMATION ===========\n")

print("Root tag:")
print(root.tag)

# Automatically detect namespace
namespace = ""

if root.tag.startswith("{"):
    namespace = root.tag.split("}")[0].strip("{")

print("\nDetected namespace:")
print(namespace if namespace else "NOT DETECTED")

ns = {'kml': namespace} if namespace else {}

print("\n=========== FOUND TAGS ===========\n")

# Tag counter
tags = Counter()

for elem in root.iter():

    tag = elem.tag

    # Clean namespace visually
    if "}" in tag:
        tag = tag.split("}")[1]

    tags[tag] += 1

for tag, count in tags.most_common():
    print(f"{tag}: {count}")

print("\n=========== DATA EXAMPLES ===========\n")

# Search Data examples
datas = root.findall(".//kml:Data", ns) if namespace else root.findall(".//Data")

if datas:

    for i, data in enumerate(datas[:20], 1):

        field_name = data.attrib.get("name")

        value = None

        for child in data:
            child_tag = child.tag.split("}")[-1]

            if child_tag == "value":
                value = child.text

        print(f"[{i}] name='{field_name}' value='{value}'")

else:
    print("No <Data> tags found")

print("\n=========== SIMPLEDATA EXAMPLES ===========\n")

simpledatas = root.findall(".//kml:SimpleData", ns) if namespace else root.findall(".//SimpleData")

if simpledatas:

    for i, sd in enumerate(simpledatas[:20], 1):

        field_name = sd.attrib.get("name")
        value = sd.text

        print(f"[{i}] name='{field_name}' value='{value}'")

else:
    print("No <SimpleData> tags found")

print("\n=========== PLACEMARK STRUCTURE ===========\n")

placemarks = root.findall(".//kml:Placemark", ns) if namespace else root.findall(".//Placemark")

if placemarks:

    example = placemarks[0]

    def print_structure(elem, level=0):

        tag = elem.tag.split("}")[-1]

        indent = "  " * level

        print(f"{indent}- {tag}")

        for child in elem:
            print_structure(child, level + 1)

    print_structure(example)

else:
    print("No Placemark elements found")

print("\n=========== FINISHED ===========\n")