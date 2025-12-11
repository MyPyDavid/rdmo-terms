import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape


def get_jinja_env():
    if os.getenv('TEMPLATE_PATH') is None:
        return Environment(
            loader=PackageLoader("terms", "templates"),
            autoescape=select_autoescape()
        )
    else:
        templates_path = Path(os.getenv('TEMPLATE_PATH'))
        return Environment(loader=FileSystemLoader(templates_path))

jinja2_env = get_jinja_env()
