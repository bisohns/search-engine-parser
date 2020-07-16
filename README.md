# Search Engine Parser

<span><i>"If it is a search engine, then it can be parsed"</i> - Some random guy</span>

![Demo](assets/animate.gif)

[![Python 3.5|3.6|3.7|3.8](https://img.shields.io/badge/python-3.5%7C3.6%7C3.7%7C3.8-blue)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/search-engine-parser.png)](https://badge.fury.io/py/search-engine-parser)
![PyPI - Downloads](https://img.shields.io/pypi/dm/search-engine-parser)
[![Build Status](https://travis-ci.com/bisoncorps/search-engine-parser.svg?branch=master)](https://travis-ci.com/bisoncorps/search-engine-parser)
[![Documentation Status](https://readthedocs.org/projects/search-engine-parser/badge/?version=latest)](https://search-engine-parser.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![All Contributors](https://img.shields.io/badge/all_contributors-10-orange.svg?style=flat-square)](#contributors)
<hr/>

Package to query popular search engines and scrape for result titles, links and descriptions. Aims to scrape the widest range of search engines.
View all [supported engines](https://github.com/bisoncorps/search-engine-parser/blob/master/docs/supported_engines.md)

- [Search Engine Parser](#search-engine-parser)
  - [Popular Supported Engines](#popular-supported-engines)
  - [Installation](#installation)
  - [Development](#development)
  - [Code Documentation](#code-documentation)
  - [Running the tests](#running-the-tests)
  - [Usage](#usage)
    - [Code](#code)
    - [Command line](#command-line)
  - [Code of Conduct](#code-of-conduct)
  - [Contribution](#contribution)
  - [License (MIT)](#license-mit) 
## Popular Supported Engines

Some of the popular search engines include:

- Google
- DuckDuckGo
- GitHub
- StackOverflow
- Baidu
- YouTube

View all [supported engines](https://github.com/bisoncorps/search-engine-parser/blob/master/docs/supported_engines.md)

## Installation

```bash
    # install only package dependencies
    pip install search-engine-parser
    # Installs `pysearch` cli  tool
    pip install "search-engine-parser[cli]"
```

## Development

Clone the repository

```bash
    git clone git@github.com:bisoncorps/search-engine-parser.git
```

Create virtual environment and install requirements

```bash
    mkvirtualenv search_engine_parser
    pip install -r requirements/dev.txt
```


## Code Documentation

Found on [Read the Docs](https://search-engine-parser.readthedocs.io/en/latest)

## Running the tests

```bash
    pytest
```

## Usage

### Code

Query Results can be scraped from popular search engines as shown in the example snippet below

```python
  import pprint

  from search_engine_parser.core.engines.bing import Search as BingSearch
  from search_engine_parser.core.engines.google import Search as GoogleSearch
  from search_engine_parser.core.engines.yahoo import Search as YahooSearch

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
      "Bing": bresults
      }

  # pretty print the result from each engine
  for k, v in a.items():
      print(f"-------------{k}------------")
      for result in v:
          pprint.pprint(result)

  # print first title from google search
  print(gresults["titles"][0])
  # print 10th link from yahoo search
  print(yresults["links"][9])
  # print 6th description from bing search
  print(bresults["descriptions"][5])

  # print first result containing links, descriptions and title
  print(gresults[0])
```

For localization, you can pass the `url` keyword and a localized url. This would use the url to query and parse using the same engine's parser
```python
  # Use google.de instead of google.com
  results = gsearch.search(*search_args, url="google.de")
```

#### Cache
The results are automatically cached for engine searches, you can either bypass cache by adding `cache=False` to the `search` or `async_search` method or clear the engines cache 
```python
    from search_engine_parser.core.engines.github import Search as GitHub
    github = GitHub()
    # bypass the cache
    github.search("search-engine-parser", cache=False)

    #OR
    # clear cache before search
    github.clear_cache()
    github.search("search-engine-parser")
```

#### Async
search-engine-parser supports `async` hence you could use codes like
```python
   results = await gsearch.async_search(*search_args)
```

#### Results
The `SearchResults` after the searching
```python
  >>> results = gsearch.search("preaching the choir", 1)
  >>> results
  <search_engine_parser.core.base.SearchResult object at 0x7f907426a280>
  # The object supports retreiving individual results by iteration of just by type (links, descriptions, titles)
  >>> results[0] # Returns the first <SearchItem>
  >>> results[0]["description"] # Get the description of the first item
  >>> results[0]["link"] # get the link of the first item
  >>> results["descriptions"] # Returns a list of all descriptions from all results
```
It can be iterated like a normal list to return individual SearchItem

### Command line

Search engine parser comes with a CLI tool known as `pysearch` e.g

```bash
pysearch --engine bing search --query "Preaching to the choir" --type descriptions
```

Result

```bash
'Preaching to the choir' originated in the USA in the 1970s. It is a variant of the earlier 'preaching to the converted', which dates from England in the late 1800s and has the same meaning. Origin - the full story 'Preaching to the choir' (also sometimes spelled quire) is of US origin.
```

![Demo](assets/example.gif)

There is a needed argument for the CLI i.e `-e Engine` followed by either of two subcommands in the CLI i.e `search` and `summary`

```bash

usage: pysearch [-h] [-u URL] [-e ENGINE] {search,summary} ...

SearchEngineParser

positional arguments:
  {search,summary}      help for subcommands
    search              search help
    summary             summary help

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     A custom link to use as base url for search e.g
                        google.de
  -e ENGINE, --engine ENGINE
                        Engine to use for parsing the query e.g google, yahoo,
                        bing,duckduckgo (default: google)
```

`summary` just shows the summary of each search engine added with descriptions on the return

```bash
pysearch --engine google summary 
```

Full arguments for the `search` subcommand shown below

```bash

usage: pysearch search [-h] -q QUERY [-p PAGE] [-t TYPE] [-r RANK]

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Query string to search engine for
  -p PAGE, --page PAGE  Page of the result to return details for (default: 1)
  -t TYPE, --type TYPE  Type of detail to return i.e full, links, desciptions
                        or titles (default: full)
  -r RANK, --rank RANK  ID of Detail to return e.g 5 (default: 0)
  -cc, --clear_cache    Clear cache of engine before searching
``` 

## Code of Conduct

All actions performed should adhere to the [code of conduct](https://github.com/bisoncorps/search-engine-parser/blob/master/CODE_OF_CONDUCT.md)


## Contribution

Before making any contribution, please follow the [contribution guide](https://github.com/bisoncorps/search-engine-parser/blob/master/CONTRIBUTING.md)

## License (MIT)

This project is opened under the [MIT 2.0 License](https://github.com/bisoncorps/search-engine-parser/blob/master/LICENSE) which allows very broad use for both academic and commercial purposes.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/Rexogamer"><img src="https://avatars0.githubusercontent.com/u/42586271?v=4" width="100px;" alt=""/><br /><sub><b>Ed Luff</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/commits?author=Rexogamer" title="Code">💻</a></td>
    <td align="center"><a href="http://diretnandomnan.webnode.com"><img src="https://avatars3.githubusercontent.com/u/23453888?v=4" width="100px;" alt=""/><br /><sub><b>Diretnan Domnan</b></sub></a><br /><a href="#infra-deven96" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=deven96" title="Tests">⚠️</a> <a href="#tool-deven96" title="Tools">🔧</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=deven96" title="Code">💻</a></td>
    <td align="center"><a href="http://mensaah.github.io"><img src="https://avatars3.githubusercontent.com/u/24734308?v=4" width="100px;" alt=""/><br /><sub><b>MeNsaaH</b></sub></a><br /><a href="#infra-MeNsaaH" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=MeNsaaH" title="Tests">⚠️</a> <a href="#tool-MeNsaaH" title="Tools">🔧</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=MeNsaaH" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/PalAditya"><img src="https://avatars2.githubusercontent.com/u/25523604?v=4" width="100px;" alt=""/><br /><sub><b>Aditya Pal</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/commits?author=PalAditya" title="Tests">⚠️</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=PalAditya" title="Code">💻</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=PalAditya" title="Documentation">📖</a></td>
    <td align="center"><a href="http://energized.pro"><img src="https://avatars1.githubusercontent.com/u/27774996?v=4" width="100px;" alt=""/><br /><sub><b>Avinash Reddy</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/issues?q=author%3AAvinashReddy3108" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/Iamdavidonuh"><img src="https://avatars3.githubusercontent.com/u/37768509?v=4" width="100px;" alt=""/><br /><sub><b>David Onuh</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/commits?author=Iamdavidonuh" title="Code">💻</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=Iamdavidonuh" title="Tests">⚠️</a></td>
    <td align="center"><a href="http://simakis.me"><img src="https://avatars2.githubusercontent.com/u/8322266?v=4" width="100px;" alt=""/><br /><sub><b>Panagiotis Simakis</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/commits?author=sp1thas" title="Code">💻</a> <a href="https://github.com/bisoncorps/search-engine-parser/commits?author=sp1thas" title="Tests">⚠️</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/reiarthur"><img src="https://avatars2.githubusercontent.com/u/20190646?v=4" width="100px;" alt=""/><br /><sub><b>reiarthur</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/commits?author=reiarthur" title="Code">💻</a></td>
    <td align="center"><a href="http://ashokkumarta.blogspot.com/"><img src="https://avatars0.githubusercontent.com/u/5450267?v=4" width="100px;" alt=""/><br /><sub><b>Ashokkumar TA</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/commits?author=ashokkumarta" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/ateuber"><img src="https://avatars2.githubusercontent.com/u/44349054?v=4" width="100px;" alt=""/><br /><sub><b>Andreas Teuber</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/commits?author=ateuber" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/mi096684"><img src="https://avatars3.githubusercontent.com/u/22032932?v=4" width="100px;" alt=""/><br /><sub><b>mi096684</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/issues?q=author%3Ami096684" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/devajithvs"><img src="https://avatars1.githubusercontent.com/u/29475282?v=4" width="100px;" alt=""/><br /><sub><b>devajithvs</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/commits?author=devajithvs" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/zakaryan2004"><img src="https://avatars3.githubusercontent.com/u/29994884?v=4" width="100px;" alt=""/><br /><sub><b>Geg Zakaryan</b></sub></a><br /><a href="https://github.com/bisoncorps/search-engine-parser/commits?author=zakaryan2004" title="Code">💻</a> <a href="https://github.com/bisoncorps/search-engine-parser/issues?q=author%3Azakaryan2004" title="Bug reports">🐛</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
