"""@desc 
		Parser for DuckDuckGo search results
"""
import re
from search_engine_parser.core.base import BaseSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError

class DuckDuckGoSearch(BaseSearch):
    """
    Searches DuckDuckGo for string
    """
    name = "DuckDuckGo"
    search_url = "https://www.duckduckgo.com/html/?q={query}"
    summary = "\tHas a number of advantages over the other search engines. \n\tIt has a clean "\
            "interface, it does not track users, it is not fully loaded with ads and has a number "\
            "of very nice features (only one page of results, you can search directly other web "\
            "sites etc).\n\tAccording to DuckDuckGo traffic stats [December, 2018], they are "\
            "currently serving more than 30 million searches per day."

    def parse_soup(self, soup):
        """
        Parses DuckDuckGo Search Soup for a query results
        """
        # find all div tags
        print(soup)
        return soup.find_all('div', class_='result')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div id="r1-{id}">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        h2 = single_result.find('h2', class_="result__title")
        link_tag = h2.find('a', class_="result__a")
        desc = single_result.find(class_='result__snippet')

        #Get the text and link
        title = link_tag.text

        # raw link is of format "/url?q=REAL-LINK&sa=..."
        link = link_tag.get('href')

        desc = desc.text
        return title, link, desc

