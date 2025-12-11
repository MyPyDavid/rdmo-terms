import os
import xml.etree.ElementTree as et
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

load_dotenv('.env')

catalog_path = Path(os.getenv('CATALOG_PATH')) / 'rdmorganiser'

public_path = Path(os.getenv('PUBLIC_PATH', 'public'))
templates_path = Path(os.getenv('TEMPLATE_PATH', 'templates'))

ns_dc = '{http://purl.org/dc/elements/1.1/}'

module_map = {
    'condition': 'conditions',
    'attribute': 'domain',
    'optionset': 'options',
    'option': 'options',
    'catalog': 'questions',
    'section': 'questions',
    'page': 'questions',
    'questionset': 'questions',
    'question': 'questions',
    'task': 'tasks',
    'view': 'views'
}

elements = []

jinja2_env = Environment(loader=FileSystemLoader(templates_path))

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

            elements.append(element)

for element in elements:
    try:
        template_path = str(Path(element['type']).with_suffix('.html'))
        template = jinja2_env.get_template(template_path)
        html = template.render(element=element)
        html_path = public_path / element['module'] / element['uri_path']
        html_path.mkdir(exist_ok=True, parents=True)
        html_path.joinpath('index.html').write_text(html)
    except TemplateNotFound:
        pass
