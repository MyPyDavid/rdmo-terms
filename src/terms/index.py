from dotenv import load_dotenv
from jinja import jinja2_env

from terms.config import base_url, public_path

load_dotenv('.env')

template_path = 'index.html'

template = jinja2_env.get_template(template_path)

html = template.render(base_url=base_url)
html_path = public_path / 'index.html'
html_path.parent.mkdir(exist_ok=True, parents=True)
html_path.write_text(html)
