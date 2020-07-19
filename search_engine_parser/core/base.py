"""@desc
		Base class inherited by every search engine
"""

import asyncio
import random
from abc import ABCMeta, abstractmethod
from contextlib import suppress
from enum import Enum, unique
from urllib.parse import urlencode, urlparse

import aiohttp
from bs4 import BeautifulSoup

from search_engine_parser.core import utils
from search_engine_parser.core.exceptions import NoResultsOrTrafficError


@unique
class ReturnType(Enum):
    FULL = "full"
    TITLE = "titles"
    DESCRIPTION = "descriptions"
    LINK = "links"


# All results returned are each items of search
class SearchItem(dict):
    """
    SearchItem is a dict of results containing keys (titles, descriptions, links and other
    additional keys dependending on the engine)
    >>> result
    <search_engine_parser.core.base.SearchItem object at 0x7f907426a280>
    >>> result["description"]
    Some description
    >>> result["descriptions"]
    Same description
    """
    def __getitem__(self, value):
        """ Allow getting by index and by type ('descriptions', 'links'...)"""
        try:
            return super().__getitem__(value)
        except KeyError:
            pass
        if not value.endswith('s'):
            value += 's'
        return super().__getitem__(value)


class SearchResult():
    """
    The SearchResults after the searching

    >>> results = gsearch.search("preaching the choir", 1)
    >>> results
    <search_engine_parser.core.base.SearchResult object at 0x7f907426a280>

    The object supports retreiving individual results by iteration of just by type
    >>> results[0] # Returns the first result <SearchItem>
    >>> results["descriptions"] # Returns a list of all descriptions from all results

    It can be iterated like a normal list to return individual SearchItem
    """

    def __init__(self):
        self.results = []

    def append(self, value):
        self.results.append(value)

    def __getitem__(self, value):
        """ Allow getting by index and by type ('descriptions', 'links'...)"""
        if isinstance(value, int):
            return self.results[value]
        l = []
        for x in self.results:
            with suppress(KeyError):
                l.append(x[value])
        return l

    def keys(self):
        keys = {}
        with suppress(IndexError):
            x = self.results[0]
            keys = x.keys()
        return keys

    def __len__(self):
        return len(self.results)

    def __repr_(self):
        return "<SearchResult: {} results>".format(len(self.results))


class BaseSearch:

    __metaclass__ = ABCMeta

    """
    Search base to be extended by search parsers
    Every subclass must have two methods `search` amd `parse_single_result`
    """
    # Summary of engine
    summary = None
    # Search Engine Name
    name = None
    # Search Engine unformatted URL
    search_url = None
    # The url after all query params have been set
    _parsed_url = None
    # boolean that indicates cache hit or miss
    _cache_hit = False

    @abstractmethod
    def parse_soup(self, soup):
        """
        Defines the results contained in a soup
        """
        raise NotImplementedError("subclasses must define method <parse_soup>")

    @abstractmethod
    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Every div/span containing a result is passed here to retrieve
        `title`, `link` and `descr`
        """
        raise NotImplementedError(
            "subclasses must define method <parse_results>")

    def get_cache_handler(self):
        """ Return Cache Handler to use"""

        return utils.CacheHandler()

    @property
    def cache_handler(self):
        return self.get_cache_handler()

    def parse_result(self, results, **kwargs):
        """
        Runs every entry on the page through parse_single_result

        :param results: Result of main search to extract individual results
        :type results: list[`bs4.element.ResultSet`]
        :returns: dictionary. Containing lists of titles, links, descriptions and other possible\
            returns.
        :rtype: dict
        """
        search_results = SearchResult()
        for each in results:
            rdict = self.parse_single_result(each, **kwargs)
            if rdict:
                search_results.append(rdict)
        return search_results

    def get_params(self, query=None, page=None, offset=None, **kwargs):
        """ This  function should be overwritten to return a dictionary of query params"""
        return {'q': query, 'page': page}

    def headers(self):
        headers = {
            "Cache-Control": 'no-cache',
            "Connection": "keep-alive",
            "User-Agent": utils.get_rand_user_agent()
        }
        return headers

    def clear_cache(self, all_cache=False):
        """
        Triggers the clear cache function for a particular engine

        :param all_cache: if True, deletes for all engines
        """
        if all_cache:
            return self.cache_handler.clear()
        return self.cache_handler.clear(self.name)

    async def get_source(self, url, cache=True):
        """
        Returns the source code of a webpage.
        Also sets the _cache_hit if cache was used

        :rtype: string
        :param url: URL to pull it's source code
        :return: html source code of a given URL.
        """
        try:
            html, cache_hit = await self.cache_handler.get_source(self.name, url, self.headers(), cache)
        except Exception as exc:
            raise Exception('ERROR: {}\n'.format(exc))
        self._cache_hit = cache_hit
        return html

    async def get_soup(self, url, cache):
        """
        Get the html soup of a query

        :rtype: `bs4.element.ResultSet`
        """
        html = await self.get_source(url, cache)
        return BeautifulSoup(html, 'lxml')

    def get_search_url(self, query=None, page=None, **kwargs):
        """
        Return a formatted search url
        """
        # Some URLs use offsets
        offset = (page * 10) - 9
        params = self.get_params(
            query=query, page=page, offset=offset, **kwargs)
        url = urlparse(self.search_url)
        # For localization purposes, custom urls can be parsed for the same engine
        # such as google.de and google.com
        if kwargs.get("url"):
            new_url = urlparse(kwargs.pop("url"))
            # When passing url without scheme e.g google.de, url is parsed as path
            if not new_url.netloc:
                url = url._replace(netloc=new_url.path)
            else:
                url = url._replace(netloc=new_url.netloc)
            self.base_url = url.geturl()
        self._parsed_url = url._replace(query=urlencode(params))

        return self._parsed_url.geturl()

    def get_results(self, soup, **kwargs):
        """ Get results from soup"""

        search_results = None
        results = self.parse_soup(soup)
        # TODO Check if empty results is caused by traffic or answers to query
        # were not found
        if not results:
            print("ENGINE FAILURE: {}\n".format(self.name))
            raise NoResultsOrTrafficError(
                "The result parsing was unsuccessful. It is either your query could not be found"
                " or it was flagged as unusual traffic")

        try:
            search_results = self.parse_result(results, **kwargs)
        # AttributeError occurs as it cannot pass the returned soup
        except AttributeError as e:
            raise NoResultsOrTrafficError(
                "The returned results could not be parsed. This might be due to site updates or "
                "server errors. Drop an issue at https://github.com/bisoncorps/search-engine-parser"
                " if this persists"
                )

        return search_results

    def search(self, query=None, page=1, cache=True, **kwargs):
        """
        Query the search engine

        :param query: the query to search for
        :type query: str
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        # Pages can only be from 1-N
        if page <= 0:
            page = 1
        # Get search Page Results
        loop = asyncio.get_event_loop()
        url = self.get_search_url(
                    query, page, **kwargs)
        soup = loop.run_until_complete(
            self.get_soup(url, cache=cache))
        return self.get_results(soup, **kwargs)

    async def async_search(self, query=None, page=1, cache=True, **kwargs):
        """
        Query the search engine but in async mode

        :param query: the query to search for
        :type query: str
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        # Pages can only be from 1-N
        if page == 0:
            page = 1
        soup = await self.get_soup(self.get_search_url(query, page, **kwargs), cache=cache)
        return self.get_results(soup, **kwargs)
