import xml.etree.ElementTree as et

from terms.config import module_map, ns_dc


def gather_elements(catalog_path):
    elements = []
    for file_path in catalog_path.rglob("*"):
        if file_path.suffix == '.xml':
            tree = et.parse(file_path)
            root_node = tree.getroot()

            for element_node in root_node:
                element = {
                    'type': element_node.tag,
                    'module': module_map[element_node.tag],
                    'uri': element_node.attrib.get(f"{ns_dc}uri")
                }

                for child_node in element_node:
                    if child_node.tag.startswith(ns_dc):
                        key = child_node.tag[len(ns_dc):]
                    elif 'lang' in child_node.attrib:
                        key = f"{child_node.tag}_{child_node.attrib['lang']}"
                    else:
                        key = child_node.tag

                    value = child_node.attrib.get(f"{ns_dc}uri") or child_node.text
                    element[key] = value

                element['url'] = f"{element['module']}/{element.get('uri_path', element.get('path', ''))}"
                elements.append(element)

    return elements
