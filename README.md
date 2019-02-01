# Search Engine Parser

Package to query popular search engines and scrape for result titles, links and descriptions

[![Build Status](https://travis-ci.com/bisoncorps/search-engine-parser.svg?branch=master)](https://travis-ci.com/bisoncorps/search-engine-parser) [![PyPI version](https://badge.fury.io/py/search-engine-parser.svg)](https://badge.fury.io/py/search-engine-parser)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

- [Search Engine Parser](#search-engine-parser)
  - [Installation](#installation)
  - [Development](#development)
  - [Documentation](#documentation)
  - [Running the tests](#running-the-tests)
  - [Usage](#usage)
  - [Contribution](#contribution)
  - [License (MIT)](#license-mit)

## Installation

```bash
    pip install search_engine_parser
```

## Development

```bash
    git clone git@github.com:bisoncorps/search-engine-parser.git
```

## Documentation

[Github Pages](https://bisoncorps.github.io/search-engine-parser)

## Running the tests

```bash
    cd search-engine-parser/
```

```bash
    python tests/__init__.py
```

## Usage

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

## Contribution

You are very welcome to modify and use them in your own projects.

Please keep a link to the [original repository](https://github.com/bisoncorps/search-engine-parser). If you have made a fork with substantial modifications that you feel may be useful, then please [open a new issue on GitHub](https://github.com/bisoncorps/search-engine-parser/issues) with a link and short description.

## License (MIT)

This project is opened under the [MIT 2.0 License](https://github.com/bisoncorps/search-engine-parser/blob/master/LICENSE) which allows very broad use for both academic and commercial purposes.
