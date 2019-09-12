# Search Engine Parser
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors)

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![PyPI version](https://badge.fury.io/py/search-engine-parser.png)](https://badge.fury.io/py/search-engine-parser)
[![Build Status](https://travis-ci.com/bisoncorps/search-engine-parser.svg?branch=master)](https://travis-ci.com/bisoncorps/search-engine-parser)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<hr/>

Package to query popular search engines and scrape for result titles, links and descriptions. Aims to scrape the widest range of search engines.

Supported Search Engines
- Google
- Yahoo
- Bing
- DuckDuckGo
- AOL



- [Search Engine Parser](#search-engine-parser)
  - [Installation](#installation)
  - [Development](#development)
  - [Code Documentation](#code-documentation)
  - [Running the tests](#running-the-tests)
  - [Usage](#usage)
    - [Code](#code)
    - [Command line](#command-line)
  - [Contribution](#contribution)
  - [License (MIT)](#license-mit)

## Installation

```bash
    pip install search-engine-parser
```

## Development

Clone the repository

```bash
    git clone git@github.com:bisoncorps/search-engine-parser.git
```

Create virtual environment and install requirements

```bash
    mkvirtualenv search_engine_parser
    pip install -r requirements-dev.txt
```


## Code Documentation

Found on [Github Pages](https://bisoncorps.github.io/search-engine-parser)

## Running the tests

```bash
    pytest
```

## Usage

### Code

Query Results can be scraped from popular search engines as shown in the example snippet below

```python
    from search_engine_parser import YahooSearch, GoogleSearch, BingSearch
    import pprint

    search_args = ('preaching to the choir', 1)
    gsearch = GoogleSearch()
    ysearch = YahooSearch()
    bsearch = BingSearch()
    gresults = gsearch.search(*search_args)
    yresults = ysearch.search(*search_args)
    bresults = bsearch.search(*search_args)
    a = {
        "Google": gresults,
        "Yahoo": yresults,
        "Bing": bresults}
    # pretty print the result from each engine
    for k, v in a.items():
        print(f"-------------{k}------------")
            pprint.pprint(v)

    # print first title from google search
    print(gresults["titles"][0])
    # print 10th link from yahoo search
    print(yresults["links"][9])
    # print 6th description from bing search
    print(bresults["descriptions"][5])
```

### Command line

Use python module runner to run the parser on the command line e.g

```bash
python -m search_engine_parser.core.cli --engine bing search --query "Preaching to the choir" --type descriptions
```

Result

```bash
'Preaching to the choir' originated in the USA in the 1970s. It is a variant of the earlier 'preaching to the converted', which dates from England in the late 1800s and has the same meaning. Origin - the full story 'Preaching to the choir' (also sometimes spelled quire) is of US origin.
```

![Demo](assets/example.gif)

There is a needed argument for the CLI i.e `-e Engine` and two subcommands in the CLI i.e `search` and `summary`

```bash

SearchEngineParser

positional arguments:
  {search,summary}      help for subcommands
    search              search help
    summary             summary help

optional arguments:
  -h, --help            show this help message and exit
  -e ENGINE, --engine ENGINE
                        Engine to use for parsing the query e.g google, yahoo,
                        bing, duckduckgo (default: google)
```

`summary` just shows the summary of each search engine added with descriptions on the return

```bash
python -m search_engine_parser.core.cli --engine google summary 
```

Full arguments for the `search` subcommand shown below

```bash

usage: cli.py search [-h] -q QUERY [-p PAGE] [-t TYPE] [-r RANK]

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Query string to search engine for
  -p PAGE, --page PAGE  Page of the result to return details for (default: 1)
  -t TYPE, --type TYPE  Type of detail to return i.e full, links, desciptions
                        or titles (default: full)
  -r RANK, --rank RANK  ID of Detail to return e.g 5 (default: 0)
```

## Contribution

You are very welcome to modify and use them in your own projects.

Please keep a link to the [original repository](https://github.com/bisoncorps/search-engine-parser). If you have made a fork with substantial modifications that you feel may be useful, then please [open a new issue on GitHub](https://github.com/bisoncorps/search-engine-parser/issues) with a link and short description and then make a pull request.

## License (MIT)

This project is opened under the [MIT 2.0 License](https://github.com/bisoncorps/search-engine-parser/blob/master/LICENSE) which allows very broad use for both academic and commercial purposes.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/Rexogamer"><img src="https://avatars0.githubusercontent.com/u/42586271?v=4" width="100px;" alt="Ed Luff"/><br /><sub><b>Ed Luff</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/commits?author=Rexogamer" title="Code">💻</a></td>
    <td align="center"><a href="http://diretnandomnan.webnode.com"><img src="https://avatars3.githubusercontent.com/u/23453888?v=4" width="100px;" alt="Diretnan Domnan"/><br /><sub><b>Diretnan Domnan</b></sub></a><br /><a href="#infra-deven96" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=deven96" title="Tests">⚠️</a> <a href="#tool-deven96" title="Tools">🔧</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=deven96" title="Code">💻</a></td>
    <td align="center"><a href="http://mensaah.github.io"><img src="https://avatars3.githubusercontent.com/u/24734308?v=4" width="100px;" alt="MeNsaaH"/><br /><sub><b>MeNsaaH</b></sub></a><br /><a href="#infra-MeNsaaH" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=MeNsaaH" title="Tests">⚠️</a> <a href="#tool-MeNsaaH" title="Tools">🔧</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=MeNsaaH" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/PalAditya"><img src="https://avatars2.githubusercontent.com/u/25523604?v=4" width="100px;" alt="Aditya Pal"/><br /><sub><b>Aditya Pal</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/commits?author=PalAditya" title="Tests">⚠️</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=PalAditya" title="Code">💻</a></td>
  </tr>
</table>

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!