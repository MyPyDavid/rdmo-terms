import os
import shutil
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv('.env')

assets = [
    ('bootstrap.min.css', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css'),
    ('bootstrap.bundle.min.js', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js'),
    ('minisearch.min.js', 'https://cdn.jsdelivr.net/npm/minisearch@7.2.0/dist/umd/index.min.js')
]

catalog_path = Path(os.getenv('CATALOG_PATH')) / 'rdmorganiser'
public_path = Path(os.getenv('PUBLIC_PATH', 'public'))
static_path = Path(os.getenv('STATIC_PATH', 'static'))

shutil.copytree(static_path, public_path / 'static', dirs_exist_ok=True)

for asset_name, asset_url in assets:
    with httpx.Client() as client:
        response = client.get(asset_url)
        response.raise_for_status()

        asset_path = public_path / 'static' / 'vendor' / asset_name
        asset_path.parent.mkdir(exist_ok=True, parents=True)
        with asset_path.open('wb') as fp:
            fp.write(response.content)
