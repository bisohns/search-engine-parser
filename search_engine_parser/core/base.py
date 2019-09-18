"""@desc 
		Base class inherited by every search engine
"""

from abc import ABCMeta, abstractmethod
import requests
import random
from bs4 import BeautifulSoup

from search_engine_parser.core.exceptions import NoResultsOrTrafficError


class BaseSearch(object):
    
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
        raise NotImplementedError("subclasses must define method <parse_results>")
    
    def parse_result(self, results):
        """
        Runs every entry on the page through parse_single_result

        :param results: Result of main search to extract individual results
        :type results: list[`bs4.element.ResultSet`]
        :returns: dictionary. Containing titles, links and descriptions.
        :rtype: dict
        """
        titles = []
        links = []
        descs = []
        for each in results:
            title = link = desc = " "
            try:
                title, link, desc = self.parse_single_result(each)
                # Append links and text to a list
                titles.append(title)
                links.append(link)
                descs.append(desc)
            except Exception as e:
                print(e)
        search_results = {'titles': titles,
                          'links': links,
                          'descriptions': descs}
        return search_results
    
    @staticmethod
    def parse_query(query):
        """
        Replace spaces in query

        :param query: query to be processed
        :type query: str
        :rtype: str
        """
        return query.replace(" ", "%20")
    
    @staticmethod
    def getSource(url):
        """
        Returns the source code of a webpage.

        :rtype: string
        :param url: URL to pull it's source code
        :return: html source code of a given URL.
        """
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        # prevent caching
        user_agent_list = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5",
            "Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5",
            ]
        headers = {
            "Cache-Control": 'no-cache',
            "Connection": "keep-alive",
            "User-Agent": random.choice(user_agent_list),
        }
        try:
            response = requests.get(url, headers=headers)
            html = response.text
        except Exception as e:
            raise Exception('ERROR: {}\n'.format(e))
        return str(html)

    def get_soup(self, url):
        """
        Get the html soup of a query

        :rtype: `bs4.element.ResultSet`
        """
        html = self.getSource(url)
        return BeautifulSoup(html, 'lxml')

    def get_search_url(self, query=None, page=None):
        """ 
        Return a formatted search url
        """
        # Some URLs use offsets
        offset = (page * 10) - 9
        return  self.search_url.format(query=query, page=page, offset=offset) 

    def search(self, query=None, page=None):
        """ 
        Query the search engine

        :param query: the query to search for 
        :type query: str
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        parsed_query = self.parse_query(query)

        # Get search Page Results
        soup = self.get_soup(self.get_search_url(parsed_query, page))
        results = self.parse_soup(soup)
        # TODO Check if empty results is caused by traffic or answers to query were not found
        if not results:
            raise NoResultsOrTrafficError(
                "The result parsing was unsuccessful. It is either your query could not be found"+
                " or it was flagged as unusual traffic")
        search_results = self.parse_result(results)
        return search_results 

