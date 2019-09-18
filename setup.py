import os
import sys
import setuptools
from setuptools.command.install import install
from search_engine_parser import __version__ as VERSION

CURRENT_DIR = os.getcwd()
REQUIREMENTS = 'requirements.txt'
requires = [line.strip('\n') for line in open(REQUIREMENTS).readlines()]

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="search-engine-parser",
    version=VERSION,
    author='Domnan Diretnan, Mmadu Manasseh',
    author_email="diretnandomnan@gmail.com",
    description="scrapes search engine pages for query titles, descriptions and links",
    url="https://github.com/bisoncorps/search-engine-parser",
    packages=setuptools.find_packages(),
    install_requires=requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords='\
        search-engine \
        search \
        parser \
        google \
        yahoo \
        bing \
        yandex',
    entry_points={
                    'console_scripts': 
                    [
                         'pysearch=search_engine_parser.core.cli:runner'
                    ]
                  },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    package_data={
        '': ['*.*'],
    },
    include_package_data=True,
)
