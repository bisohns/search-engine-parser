"""@desc
		Parser for DuckDuckGo search results
"""
import re
from search_engine_parser.core.base import BaseSearch


class DuckDuckGoSearch(BaseSearch):
    """
    Searches DuckDuckGo for string
    """
    name = "DuckDuckGo"
    base_url = "https://www.duckduckgo.com"
    search_url = "https://www.duckduckgo.com/html/?q={query}&s={start}&dc={offset}&v=l&o=json&api=/d.js"
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
        return soup.find_all('div', class_='result')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div id="r1-{id}">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        h2 = single_result.find('h2', class_="result__title") #pylint: disable=invalid-name
        link_tag = single_result.find('a', class_="result__url")
        desc = single_result.find(class_='result__snippet')

        # Get the text and link
        title = h2.text.strip()

        # raw link is of format "/url?q=REAL-LINK&sa=..."
        raw_link = self.base_url + link_tag.get('href')
        
        re_str = re.findall("uddg=(.+)", raw_link)[0]
        re_str = re_str.replace("%3A", ":")
        link = re_str.replace("%2F", "/")
        link = link.replace("%2D", "-")

        desc = desc.text
        rdict = {
            "titles": title,
            "links": link,
            "descriptions": desc,
        }
        return rdict

    def get_search_url(self, query=None, page=None, **kwargs):
        """
        Return a formatted search url
        """
        # Start value for the page
        start = 0 if (page < 2) else (((page-1) * 50) - 20)

        type_ = self.keywords.get("type", None)

        return self.search_url.format(
            query=query,
            start=start,
            offset=start-1,
            type_=type_,
            )
