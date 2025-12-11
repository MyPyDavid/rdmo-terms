import asyncio
import os
import shutil
from importlib.resources import files as importlib_files
from pathlib import Path

import httpx
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

from .config import assets


def gather_files(catalog_path: Path) -> list[Path]:
    return sorted(
        [file_path for file_path in catalog_path.rglob("*.xml") if file_path.is_file()]
    )


def get_template_env():
    templates_path = os.getenv('TEMPLATE_PATH')
    if templates_path is None:
        env = Environment(loader=PackageLoader("terms", "templates"), autoescape=select_autoescape())
    else:
        env = Environment(loader=FileSystemLoader(templates_path))

    return env


def copy_static(static_path: Path):
    shutil.copytree(str(importlib_files('terms') / 'static'), static_path, dirs_exist_ok=True)


async def download_assets(assets_path: Path) -> None:
    async with httpx.AsyncClient() as client:
        await asyncio.gather(
            *[
                download_asset(client, asset_name, asset_url, assets_path)
                for asset_name, asset_url in assets
            ]
        )


async def download_asset(client: httpx.AsyncClient, asset_name: str, asset_url: str, assets_path: Path) -> None:
    response = await client.get(asset_url)
    response.raise_for_status()

    asset_path = assets_path / asset_name
    asset_path.parent.mkdir(exist_ok=True, parents=True)
    asset_path.write_bytes(response.content)
