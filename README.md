# rdmo-terms

[RDMO](https://github.com/rdmorganiser/rdmo) is a tool to support the systematic planning,
organisation and implementation of the data management throughout the course of a research project.

This repo is used to create https://rdmorganiser.github.io/terms/, which can be used as
a search and filter interface for the central content repository for RDMO located at
<https://github.com/rdmorganiser/rdmo-catalog>.

## Setup

```bash
pip install -e .
```

Create `.env` with:

```
CATALOG_PATH=../rdmo-catalog/rdmorganiser
```

## Usage

```bash
rdmo-terms build     # shortcut for index, elements, element, static, and assets
rdmo-terms index     # create the html and the json file containing all elements
rdmo-terms elements  # create one html and one json file for each module
rdmo-terms element   # create one html and one json file for each element
rdmo-terms static    # copy files from static to the public dir
rdmo-terms assets    # download 3rd party assets from CDN
rdmo-terms clean     # remove the public dir
rdmo-terms serve     # serve the public dir to http://localhost:4000
```
