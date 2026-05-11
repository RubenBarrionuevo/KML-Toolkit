import xml.etree.ElementTree as ET

input_file = "input.kml"
output_file = "output.kml"

# Target text used to find and remove placemarks
target_text = "N-340"

# Parse KML
tree = ET.parse(input_file)
root = tree.getroot()

# Namespace
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

removed = 0

# Search ALL elements that may contain Placemark nodes
for parent in root.iter():

    # Get DIRECT Placemark children
    placemarks = parent.findall("kml:Placemark", ns)

    for placemark in placemarks:

        delete = False

        # Find all Data elements inside the Placemark
        data_elements = placemark.findall(".//kml:Data", ns)

        for data in data_elements:

            field_name = data.attrib.get("name")

            # Only interested in "Filter value"
            if field_name == "Filter value":

                value_elem = data.find("kml:value", ns)

                if value_elem is not None:

                    # Get clean text
                    value = "".join(value_elem.itertext()).strip()

                    print(f"Detected: {value}")

                    if value == target_text:
                        delete = True
                        break

        # Remove complete Placemark
        if delete:
            parent.remove(placemark)
            removed += 1

print(f"\nTotal removed: {removed}")

# Save new KML
tree.write(
    output_file,
    encoding="utf-8",
    xml_declaration=True
)

print(f"KML saved to: {output_file}")