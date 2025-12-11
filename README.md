# rdmo-terms

RDMO is a tool to support the systematic planning, organisation and implementation of the data management throughout the course of a research project. On this page, we offer a search and filter interface for the central content repository for RDMO located at <https://github.com/rdmorganiser/rdmo-catalog>.

## Setup

```bash
pip install -e .
```

Create `.env` with:

```
CATALOG_PATH=../rdmo-catalog
```

## Usage

```bash
python src/terms/elements.py
python src/terms/index.py
```
