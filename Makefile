all: html build install pypi

html: Makefile
	sphinx-build -M html source build;\
    rm -rf docs;\
    cp -r build/html docs;

build: setup.py
	python setup.py sdist bdist_wheel

pypi: setup.py
	python setup.py sdist upload

install: setup.py
	python setup.py install
