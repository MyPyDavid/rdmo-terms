.PHONY: index element elements static serve clean

all: index element elements static

index:
	python src/terms/index.py

element:
	python src/terms/element.py

elements:
	python src/terms/elements.py

static:
	python src/terms/static.py

serve:
	python3 -m http.server 4000 -d public

clean:
	rm -r public
