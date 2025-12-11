from collections import defaultdict
from pathlib import Path

from config import base_url, catalog_path, public_path
from jinja import jinja2_env
from jinja2.exceptions import TemplateNotFound
from utils import gather_elements

module_elements = defaultdict(list)
for element in gather_elements(catalog_path):
    module_elements[element.module].append(element)

for module, elements in module_elements.items():
    template_path = str(Path(module).with_suffix('.html'))
    try:
        template = jinja2_env.get_template(template_path)
    except TemplateNotFound:
        template = jinja2_env.get_template('elements.html')

    html = template.render(base_url=base_url, elements=elements)
    html_path = public_path / module
    html_path.mkdir(exist_ok=True, parents=True)
    html_path.joinpath('index.html').write_text(html)
