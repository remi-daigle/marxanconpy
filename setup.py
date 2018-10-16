import setuptools
import marxanconpy

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='marxanconpy',
    version=marxanconpy.__version__.replace("v",""),
    author='Remi Daigle',
    author_email='remi.daigle@dal.ca',
    description="The python package for Marxan Connect",
    long_description=long_description,
    long_description_content_type="markdown",
    url="https://remi-daigle.github.io/marxanconpy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)