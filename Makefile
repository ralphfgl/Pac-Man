
install:
	pip install -r requirements.txt

run:
	python3 pac_moul.py config.json

build:
	rm -rf build dist
	python3 -m PyInstaller --onefile \
		--windowed \
		--name pac_moul \
		--add-data "asset:asset" \
		--add-data "config.json:." \
		--add-data "highscores.json:." \
		pac_moul.py
	cp config.json dist/
	cp README.txt dist/
	cp asset/ dist/ -r
	zip -r pac_moul_linux.zip dist/

debug:
	python3 -m pdb pac_moul.py config.json

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	flake8 pacmoulinette/ pac_moul.py
	mypy pacmoulinette/ pac_moul.py --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 pacmoulinette/ pac_moul.py
	mypy pacmoulinette/ pac_moul.py --strict

.PHONY: install run debug clean lint build
