import asyncio
import os
import shutil
from importlib.resources import files
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv('.env')

catalog_path = Path(os.getenv('CATALOG_PATH')) / 'rdmorganiser'
public_path = Path(os.getenv('PUBLIC_PATH', 'public'))

assets = [
    ('bootstrap.min.css', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css'),
    ('bootstrap.min.css.map', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css.map'),
    ('bootstrap.bundle.min.js', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js'),
    ('minisearch.min.js', 'https://cdn.jsdelivr.net/npm/minisearch@7.2.0/dist/umd/index.min.js')
]


def copytree_traversable(src, dst: Path) -> None:
    """
    Recursively copy from a Traversable (importlib.resources) or Path into dst.
    Existing directories are kept (like dirs_exist_ok=True).
    """
    dst.mkdir(parents=True, exist_ok=True)

    for entry in src.iterdir():
        target = dst / entry.name
        if entry.is_dir():
            copytree_traversable(entry, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with entry.open("rb") as fsrc, target.open("wb") as fdst:
                shutil.copyfileobj(fsrc, fdst)


def copy_static(public_path: Path) -> None:
    # Optional override for local dev:
    static_override = os.getenv("STATIC_PATH")

    if static_override:
        # From a real filesystem directory
        src_root = Path(static_override)
    else:
        # From the installed package: terms/static
        src_root = files("terms") / "static"

    dst_root = public_path / "static"
    copytree_traversable(src_root, dst_root)


async def download_asset(client: httpx.AsyncClient, asset_name: str, asset_url: str, public_path: Path) -> None:
    response = await client.get(asset_url)
    response.raise_for_status()

    asset_path = public_path / "static" / "vendor" / asset_name
    asset_path.parent.mkdir(exist_ok=True, parents=True)
    asset_path.write_bytes(response.content)


async def download_assets(public_path: Path) -> None:
    async with httpx.AsyncClient() as client:
        await asyncio.gather(
            *[
                download_asset(client, asset_name, asset_url, public_path)
                for asset_name, asset_url in assets
            ]
        )


async def main() -> None:
    # 1. Copy packaged static files → public/static
    copy_static(public_path)

    # 2. Download CDN assets (concurrently)
    await download_assets(public_path)


if __name__ == "__main__":
    asyncio.run(main())
