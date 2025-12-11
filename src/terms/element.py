from pathlib import Path

from config import base_url, catalog_path, public_path
from jinja import jinja2_env
from jinja2.exceptions import TemplateNotFound
from utils import gather_elements

for element in gather_elements(catalog_path):
    template_path = str(Path(element['type']).with_suffix('.html'))
    try:
        template = jinja2_env.get_template(template_path)
    except TemplateNotFound:
        template = jinja2_env.get_template('element.html')

    html = template.render(base_url=base_url, element=element)
    html_path = public_path / element['url']
    html_path.mkdir(exist_ok=True, parents=True)
    html_path.joinpath('index.html').write_text(html)
    html_path.joinpath('index.json').write_text(json.dumps(element, indent=2))
