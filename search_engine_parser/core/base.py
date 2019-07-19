"""@desc 
		Base class inherited by every search engine

 	@author 
 		Domnan Diretnan
 		Artificial Intelligence Enthusiast & Software Engineer.
 		Email: diretnandomnan@gmail.com
 		Github: https://github.com/deven96
 		GitLab: https://gitlab.com/Deven96

 	@project
 		@create date 2019-02-01 22:15:44
 		@modify date 2019-02-01 22:15:44

	@license
		MIT License
		Copyright (c) 2018. Domnan Diretnan. All rights reserved

 """
from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
from consts import SEARCH_QUERY
import requests

class BaseSearch(object):
    
    __metaclass__ = ABCMeta

    """
    Search base to be extended by search parsers
    Every subclass must have two methods `search` amd `parse_single_result`
    """

    @abstractmethod
    def search(self, query, page=1):
        """
        Master method coordinating search parsing
        """
        raise NotImplementedError("subclasses must define method <search>")

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
                ''' Append links and text to a list '''
                titles.append(title)
                links.append(link)
                descs.append(desc)
            except Exception as e:
                print(e)
                pass
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
        import requests
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        # prevent caching
        headers = {
            "Cache-Control": 'no-cache',
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            html = response.text
        except Exception as e:
            raise Exception('ERROR: {}\n'.format(e))
        return str(html)

    @staticmethod
    def get_soup(raw_query, engine="Google", page=1):
        """
        Get the html soup of a query

        :param raw_query: unprocessed query string
        :type raw_query: str
        :param engine: search engine to make use of, defaults to google
        :type engine: str
        :param page: page to return
        :type page: int
        :rtype: `bs4.element.ResultSet`
        """
        # replace spaces in string
        query = BaseSearch.parse_query(raw_query)
        search_fmt_string = SEARCH_QUERY[engine]
        if engine == "Google":
            search_url = search_fmt_string.format(query, page)
        if engine == "Yahoo":
            offset = (page * 10) - 9
            search_url = search_fmt_string.format(query, offset)
        if engine == "Bing":
            # structure pages in terms of 
            first= (page * 10) - 9
            search_url = search_fmt_string.format(query, first)
        html = BaseSearch.getSource(search_url)
        return BeautifulSoup(html, 'lxml')