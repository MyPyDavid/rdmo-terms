.PHONY: index element elements static

all: index element elements static

index:
	python build/index.py

element:
	python build/element.py

elements:
	python build/elements.py

static:
	python build/static.py

clean:
	rm -r public
