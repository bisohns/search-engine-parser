"""@desc
		Parser for DuckDuckGo search results
"""
from search_engine_parser.core.base import BaseSearch


class DuckDuckGoSearch(BaseSearch):
    """
    Searches DuckDuckGo for string
    """
    name = "DuckDuckGo"
    base_url = "https://www.duckduckgo.com"
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
        return soup.find_all('div', class_='result')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div id="r1-{id}">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        h2 = single_result.find('h2', class_="result__title")
        link_tag = single_result.find('a', class_="result__url")
        desc = single_result.find(class_='result__snippet')

        # Get the text and link
        title = h2.text.strip()

        # raw link is of format "/url?q=REAL-LINK&sa=..."
        link = self.base_url + link_tag.get('href')

        desc = desc.text
        rdict = {
            "titles": title,
            "links": link,
            "descriptions": desc,
        }
        return rdict
