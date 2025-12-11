from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as et

from terms.config import module_map, ns_dc


@dataclass
class Reference:
    uri: str
    url: str | None = None

    def to_serializable(self) -> dict[str, str]:
        return {'uri': self.uri, 'url': self.url}


@dataclass
class Element:
    uri: str
    type: str
    module: str
    attributes: dict[str, Any] = field(default_factory=dict)
    url: str | None = None

    def to_serializable(self) -> dict[str, Any]:
        base = {'uri': self.uri, 'type': self.type, 'module': self.module, 'url': self.url}
        base.update({key: self._serialize_value(value) for key, value in self.attributes.items()})
        return base

    def _serialize_value(self, value: Any) -> Any:
        if isinstance(value, Reference):
            return value.to_serializable()
        if isinstance(value, list):
            return [self._serialize_value(item) for item in value]
        return value


def gather_elements(files: list[Path]) -> list:
    elements = []
    urls = {}
    for file_path in files:
        tree = et.parse(file_path)
        root_node = tree.getroot()

        for element_node in root_node:
            uri = element_node.attrib.get(f"{ns_dc}uri")
            element = Element(uri=uri, type=element_node.tag, module=module_map[element_node.tag])

            for child_node in element_node:
                key = _extract_key(child_node)

                if len(child_node) > 0:
                    element.attributes[key] = [
                        Reference(uri=grand_child_node.attrib.get(f"{ns_dc}uri"))
                        for grand_child_node in child_node
                    ]
                elif child_node.attrib.get(f"{ns_dc}uri"):
                    element.attributes[key] = Reference(uri=child_node.attrib.get(f"{ns_dc}uri"))
                else:
                    element.attributes[key] = child_node.text

            element.url = f"{element.module}/{element.attributes.get('uri_path', element.attributes.get('path', ''))}"
            urls[element.uri] = element.url
            elements.append(element)

    # loop over subvalues again and add urls
    for element in elements:
        _attach_urls(element.attributes.values(), urls)

    return sorted([element.to_serializable() for element in elements], key=lambda x: x["uri"])


def _extract_key(child_node: et.Element) -> str:
    if child_node.tag.startswith(ns_dc):
        return child_node.tag[len(ns_dc):]
    if 'lang' in child_node.attrib:
        return f"{child_node.tag}_{child_node.attrib['lang']}"
    return child_node.tag


def _attach_urls(values: Iterable[Any], urls: dict[str, str]) -> None:
    for value in values:
        if isinstance(value, list):
            for item in value:
                if isinstance(item, Reference):
                    item.url = urls.get(item.uri)
        elif isinstance(value, Reference):
            value.url = urls.get(value.uri)
