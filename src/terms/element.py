import os
from pathlib import Path

from dotenv import load_dotenv
from jinja import jinja2_env
from jinja2.exceptions import TemplateNotFound
from utils import gather_elements

load_dotenv('.env')

base_url = os.getenv('BASE_URL', '/')

catalog_path = Path(os.getenv('CATALOG_PATH')) / 'rdmorganiser'

public_path = Path(os.getenv('PUBLIC_PATH', 'public'))

for element in gather_elements(catalog_path):
    template_path = str(Path(element.type).with_suffix('.html'))
    try:
        template = jinja2_env.get_template(template_path)
    except TemplateNotFound:
        template = jinja2_env.get_template('element.html')

    html = template.render(base_url=base_url, element=element)
    html_path = public_path / element.url
    html_path.mkdir(exist_ok=True, parents=True)
    html_path.joinpath('index.html').write_text(html)
