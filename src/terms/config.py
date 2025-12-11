import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv('.env')

base_url = os.getenv('BASE_URL', '/')
catalog_path = Path(os.getenv('CATALOG_PATH')) / 'rdmorganiser'
public_path = Path(os.getenv('PUBLIC_PATH', 'public'))

assets = [
    ('bootstrap.min.css', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css'),
    ('bootstrap.min.css.map', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css.map'),
    ('bootstrap.bundle.min.js', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js'),
    ('minisearch.min.js', 'https://cdn.jsdelivr.net/npm/minisearch@7.2.0/dist/umd/index.min.js')
]
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
