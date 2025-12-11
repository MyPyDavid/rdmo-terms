import json

from dotenv import load_dotenv
from jinja import jinja2_env

from terms.config import base_url, catalog_path, public_path

from utils import gather_elements

load_dotenv('.env')

template_path = 'index.html'

template = jinja2_env.get_template(template_path)

elements = gather_elements(catalog_path)

html = template.render(base_url=base_url, elements=elements)
html_path = public_path / 'index.html'
html_path.parent.mkdir(exist_ok=True, parents=True)
html_path.write_text(html)
html_path.with_suffix('.json').write_text(json.dumps(elements, indent=2))
