all: html install pypi

html: Makefile
	jupyter nbconvert --to rst source/example.ipynb
	sphinx-build -M html source build;\
    rm -rf docs;\
    cp -r build/html docs;

build: setup.py
	rm -rf dist/*
	python setup.py sdist

pypi: build setup.py
	python setup.py sdist upload

install: build setup.py
	pip uninstall marxanconpy;\
	pip install dist/marxanconpy-0.1.2b4.tar.gz