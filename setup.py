import re
import setuptools

REQUIREMENTS = 'requirements/main.txt'
CLI_REQUIREMENTS = 'requirements/cli.txt'

REQUIRED_PYTHON = (3, 5)

requires = [line.strip('\n') for line in open(REQUIREMENTS).readlines()]
requires_cli = [line.strip('\n') for line in open(CLI_REQUIREMENTS).readlines()]

with open("README.md", "r") as fh:
    long_description = fh.read()

# Trying to load version directly from `search-engine-parser` module attempts
# to load __init__.py which will try to load other libraries not yet installed
with open("search_engine_parser/__init__.py", "rt", encoding="utf8") as f:
    VERSION = re.search(r'__version__ = "(.*?)"', f.read(), re.M).group(1)

setuptools.setup(
    name="search-engine-parser",
    version=VERSION,
    author='Domnan Diretnan, Mmadu Manasseh',
    author_email="diretnandomnan@gmail.com",
    description="scrapes search engine pages for query titles, descriptions and links",
    url="https://github.com/bisoncorps/search-engine-parser",
    project_urls={
        "documentation":"https://search-engine-parser.readthedocs.io/en/latest",
        "source": "https://github.com/bisoncorps/search-engine-parser",
    },
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
        yandex \
        stackoverflow \
        github \
        baidu ',
    entry_points={'console_scripts': [
        'pysearch=search_engine_parser.core.cli:runner'
    ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        '': ['*.*'],
    },
    include_package_data=True,
    extras_require={
        'cli': requires_cli
    },
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
)
