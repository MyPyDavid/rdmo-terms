import xml.etree.ElementTree as et

from terms.config import module_map, ns_dc

def gather_elements(catalog_path):
    elements = []
    urls = {}
    for file_path in catalog_path.rglob("*"):
        if file_path.suffix == '.xml':
            tree = et.parse(file_path)
            root_node = tree.getroot()

            for element_node in root_node:
                uri = element_node.attrib.get(f"{ns_dc}uri")
                element = {
                    'uri': uri,
                    'type': element_node.tag,
                    'module': module_map[element_node.tag],
                }

                for child_node in element_node:
                    if child_node.tag.startswith(ns_dc):
                        key = child_node.tag[len(ns_dc):]
                    elif 'lang' in child_node.attrib:
                        key = f"{child_node.tag}_{child_node.attrib['lang']}"
                    else:
                        key = child_node.tag

                    if len(child_node) > 0:
                        element[key] = [{
                            'uri': grand_child_node.attrib.get(f"{ns_dc}uri") for grand_child_node in child_node
                        }]
                    elif child_node.attrib.get(f"{ns_dc}uri"):
                        element[key] = {
                            'uri': child_node.attrib.get(f"{ns_dc}uri")
                        }
                    else:
                        element[key] = child_node.text

                urls[uri] = element['url'] = f"{element['module']}/{element.get('uri_path', element.get('path', ''))}"
                elements.append(element)

    # loop over subvalues again and add urls
    for element in elements:
        for key in element.keys():
            if isinstance(element[key], list):
                for item in element[key]:
                    item['url'] = urls[item['uri']]
            if isinstance(element[key], dict):
                element[key]['url'] = urls[item['uri']]

    return sorted(elements, key=lambda x: x["uri"])
