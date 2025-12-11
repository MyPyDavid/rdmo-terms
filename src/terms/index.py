import os
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv('.env')

base_url = os.getenv('BASE_URL', '/')

catalog_path = Path(os.getenv('CATALOG_PATH')) / 'rdmorganiser'

public_path = Path(os.getenv('PUBLIC_PATH', 'public'))
templates_path = Path(os.getenv('TEMPLATE_PATH', 'templates'))

jinja2_env = Environment(loader=FileSystemLoader(templates_path))

template_path = 'index.html'
template = jinja2_env.get_template(template_path)

html = template.render(base_url=base_url)
html_path = public_path / 'index.html'
html_path.parent.mkdir(exist_ok=True, parents=True)
html_path.write_text(html)
