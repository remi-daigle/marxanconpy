all: html build install pypi

html: Makefile
	jupyter nbconvert --to rst source/example.ipynb
	sphinx-build -M html source build;\
    rm -rf docs;\
    cp -r build/html docs;

build: setup.py
	python setup.py sdist bdist_wheel

pypi: setup.py
	python setup.py bdist upload

install: setup.py
	pip uninstall marxanconpy
	python setup.py install
