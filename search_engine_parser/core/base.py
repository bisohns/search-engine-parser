"""@desc
		Base class inherited by every search engine
"""

from abc import ABCMeta, abstractmethod
import random
import asyncio
import aiohttp
from bs4 import BeautifulSoup

from search_engine_parser.core.exceptions import NoResultsOrTrafficError


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

    @abstractmethod
    def parse_soup(self, soup):
        """
        Defines the results contained in a soup
        """
        raise NotImplementedError("subclasses must define method <parse_soup>")

    @abstractmethod
    def parse_single_result(self, single_result):
        """
        Every div/span containing a result is passed here to retrieve
        `title`, `link` and `descr`
        """
        raise NotImplementedError(
            "subclasses must define method <parse_results>")

    def parse_result(self, results):
        """
        Runs every entry on the page through parse_single_result

        :param results: Result of main search to extract individual results
        :type results: list[`bs4.element.ResultSet`]
        :returns: dictionary. Containing lists of titles, links, descriptions and other possible\
            returns.
        :rtype: dict
        """
        search_results = dict()
        for each in results:
            try:
                rdict = self.parse_single_result(each)
                # Create a list for all keys in rdict if not exist, else
                for key in rdict.keys():
                    if key not in search_results.keys():
                        search_results[key] = list([rdict[key]])
                    else:
                        search_results[key].append(rdict[key])
            except Exception: #pylint: disable=invalid-name, broad-except
                pass
        return search_results

    @staticmethod
    def parse_query(query):
        """
        Replace spaces in query

        :param query: query to be processed
        :type query: str
        :rtype: str
        """
        return query.replace(" ", "%20").replace(":", "%3A")

    @staticmethod
    async def get_source(url):
        """
        Returns the source code of a webpage.

        :rtype: string
        :param url: URL to pull it's source code
        :return: html source code of a given URL.
        """
        # headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        # prevent caching
        user_agent_list = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/72.0.3626.121 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) "
            "Chrome/19.0.1084.46 Safari/536.5",
            "Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) "
            "Chrome/19.0.1084.46 Safari/536.5",
        ]
        headers = {
            "Cache-Control": 'no-cache',
            "Connection": "keep-alive",
            "User-Agent": random.choice(user_agent_list),
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    html = await resp.text()
        except Exception as exc:
            raise Exception('ERROR: {}\n'.format(exc))
        return str(html)

    async def get_soup(self, url):
        """
        Get the html soup of a query

        :rtype: `bs4.element.ResultSet`
        """
        html = await self.get_source(url)
        return BeautifulSoup(html, 'lxml')

    def get_search_url(self, query=None, page=None, **kwargs):
        """
        Return a formatted search url
        """
        # Some URLs use offsets
        offset = (page * 10) - 9
        type_ = self.keywords.get("type", None)

        return self.search_url.format(
            query=query,
            page=page,
            offset=offset,
            type_=type_,
            )

    def get_results(self, soup):
        """ Get results from soup"""

        results = self.parse_soup(soup)
        # TODO Check if empty results is caused by traffic or answers to query
        # were not found
        if not results:
            raise NoResultsOrTrafficError(
                "The result parsing was unsuccessful. It is either your query could not be found" +
                " or it was flagged as unusual traffic")
        search_results = self.parse_result(results)
        return search_results

    def search(self, query=None, page=None, **kwargs):
        """
        Query the search engine

        :param query: the query to search for
        :type query: str
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        parsed_query = self.parse_query(query)
        # save kwargs as self variable
        self.keywords = kwargs
        # Get search Page Results
        loop = asyncio.get_event_loop()
        soup = loop.run_until_complete(
            self.get_soup(
                self.get_search_url(
                    query, page, **kwargs)))
        return self.get_results(soup)

    async def async_search(self, query=None, page=None, callback=None, **kwargs):
        """
        Query the search engine but in async mode

        :param query: the query to search for
        :type query: str
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :param callback: The callback function to execute when results are returned
        :type page: function
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        # TODO callback should be called
        if callback:
            pass
        self.keywords = kwargs        
        parsed_query = self.parse_query(query)
        soup = await self.get_soup(self.get_search_url(parsed_query, page))
        return self.get_results(soup)
