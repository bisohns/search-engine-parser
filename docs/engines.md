## Engines

This document is dedicated to helping developers better understand how to include Engines to the SearchEngineParser OSS.

### What Search Engines are accepted

This project was started primarily for general purpose search engines like Google and Bing.
It has since surpassed that and aims to include all useful sites (termed `custom engines`).
These custom engines include things like Youtube, GitHub, StackOverflow, e.t.c.
Basically any site that is popular enough to search and return links

### Skills Needed

- Python (obviously)
- Sphinx
- Regular Expressions
- Beautiful Soup

### Implementing an Engine

The engine modules are in the [search_engine_parser/core/engines/](https://github.com/bisoncorps/search-engine-parser/blob/master/search_engine_parser/core/engines) directory

* Create module for the new search engine

* Create class for the Engine

* Class should import from the base engine

* Example for a fake engine is shown below

```python

    # fake.py
    from search_engine_parser.core.base import BaseSearch
    from search_engine_parser.core.exceptions import NoResultsOrTrafficError

    class FakeEngine(BaseSearch):
        # name of the engine to be displayed on the CLI, preferably PascalCase
        name = "FakeEngine"
        # engine url to be search, with parameters to be formatted e.g query , page
        search_url = "https://search.fake.com/fake/search"
        # a short 2 or 3 line summary of the engine with some statistics, preferably obtained from wikipedia
        summary = "\t According to netmarketshare, this site is balderdash among "\
	      "search engines with a market share that is close to 100%. "\
	      "The fake engine includes many popular features but was solely created to show you an example ."

        
        # this function should return the dict of params to be passed to the search_url
        def get_params(self, query=None, page=None, offset=None, **kwargs):
          params = {}
          params["q"] =query
          params["page"] = page
          return params

        # This function should use beautiful soup (combined with regex if necessary) 
        # to return all the divs containiing results
        def parse_soup(self, soup):
            return soup.find_all('div', class_='fake-result-div')
        
        # This function should parse each result soup to return title, link, and description 
        # NOTE: The implementation may not be as straightforward as shown below
        def parse_single_result(self, single_result):
            title_div = single_result.find('div', class_='fake-title')
            title = title_div.text
            link_tag = title_div.find('a')
            link = link_tag.get('href')
            desc_span = single_result.find('span', class_='fake-description')
            desc = desc.text
            rdict = {
                "titles": title,
                "links": link,
                "descriptions": desc,
            }
            return rdict
```

* Import the engine by adding to the following files

[search_engine_parser/__init__.py](https://github.com/bisoncorps/search-engine-parser/blob/master/search_engine_parser/__init__.py)

```python
    ...
    from search_engine_parser.core.engines.fake import Search as FakeEngineSearch
```


* Make sure to write code documentation by following the [documentation guide](https://github.com/bisoncorps/search-engine-parser/blob/master/docs/documentation.md#documenting-an-engine)

* [Generate the RST file](https://github.com/bisoncorps/search-engine-parser/blob/master/docs/documentation.md#generating-the-files)

* Add Engine to Supported Engines in [supported engines](https://github.com/bisoncorps/search-engine-parser/blob/master/docs/supported_engines.md)
