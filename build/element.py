import os

from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from utils import gather_elements

load_dotenv('.env')

catalog_path = Path(os.getenv('CATALOG_PATH')) / 'rdmorganiser'

public_path = Path(os.getenv('PUBLIC_PATH', 'public'))
templates_path = Path(os.getenv('TEMPLATE_PATH', 'templates'))

jinja2_env = Environment(loader=FileSystemLoader(templates_path))

for element in gather_elements(catalog_path):
    template_path = str(Path(element.type).with_suffix('.html'))
    try:
        template = jinja2_env.get_template(template_path)
    except TemplateNotFound:
        template = jinja2_env.get_template('element.html')

    html = template.render(element=element)
    html_path = public_path / element.file_path
    html_path.mkdir(exist_ok=True, parents=True)
    html_path.joinpath('index.html').write_text(html)
