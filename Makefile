all: html install pypi

html: Makefile
	jupyter nbconvert --to rst source/example_marcon.ipynb
	sphinx-build -M html source build;\
    rm -rf docs;\
    cp -r build/html docs;

marxanconpy: marxanconpy/__init__.py \
    marxanconpy/manipulation.py \
    marxanconpy/marcon.py \
    marxanconpy/metrics.py \
    marxanconpy/posthoc.py \
    marxanconpy/spatial.py

build: setup.py marxanconpy
	rm -rf dist/*
	python setup.py sdist

pypi: build setup.py
	python setup.py sdist upload

install: build setup.py
	pip uninstall marxanconpy -y;\
	pip install dist/marxanconpy-*.tar.gz