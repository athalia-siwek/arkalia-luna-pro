# 📦 Makefile Arkalia IA Devstation

.PHONY: all test format bump patch minor major

all: test

test:
	pytest

format:
	black .
	ruff check . --fix

bump:
	bumpver update

patch:
	bumpver update --patch

minor:
	bumpver update --minor

major:
	bumpver update --major
