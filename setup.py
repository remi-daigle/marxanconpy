import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='marxanconpy',
    version='0.1.2b1',
    author='Remi Daigle',
    author_email='remi.daigle@dal.ca',
    description="The python package for Marxan Connect",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://remi-daigle.github.io/marxanconpy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)