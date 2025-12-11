.PHONY: index element elements static serve clean

all: index element elements static

index:
	python build/index.py

element:
	python build/element.py

elements:
	python build/elements.py

static:
	python build/static.py

serve:
	python3 -m http.server 4000 -d public

clean:
	rm -r public
