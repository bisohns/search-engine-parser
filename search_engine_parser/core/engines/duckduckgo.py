"""@desc
		Parser for DuckDuckGo search results
"""
import re

from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem
from search_engine_parser.core import utils


class Search(BaseSearch):
    """
    Searches DuckDuckGo for string
    """
    name = "DuckDuckGo"
    base_url = "https://www.duckduckgo.com"
    search_url = "https://www.duckduckgo.com/html?"
    summary = "\tHas a number of advantages over the other search engines. \n\tIt has a clean "\
        "interface, it does not track users, it is not fully loaded with ads and has a number "\
        "of very nice features (only one page of results, you can search directly other web "\
        "sites etc).\n\tAccording to DuckDuckGo traffic stats [December, 2018], they are "\
        "currently serving more than 30 million searches per day."

    def get_params(self, query=None, page=None, offset=None, **kwargs):
        page_code = 0 if (page < 1) else (50 * (page - 1) + 30)
        params = {}
        params["q"] = query
        params["s"] = str(page_code)
        params["nextParams"] = ''
        params["v"] = "l"
        params["o"] = "json"
        params["dc"] = str(page_code+1)
        params["kf"] = '-1'  # Disable favicons
        params["kh"] = '1'  # HTTPS always ON
        params["k1"] = '-1'  # Advertisements off
     
        return params

    def parse_soup(self, soup):
        """
        Parses DuckDuckGo Search Soup for a query results
        """
        # find all div tags
        return soup.find_all('div', class_='result')

    def parse_single_result(self, single_result, return_type=ReturnType.FULL):
        """
        Parses the source code to return

        :param single_result: single result found in <div id="r1-{id}">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """

        rdict = SearchItem()

        if return_type in (ReturnType.FULL, return_type.TITLE):
            h2 = single_result.find(
                'h2', class_="result__title")  # pylint: disable=invalid-name
            # Get the text and link
            rdict["titles"] = h2.text.strip()

        if return_type in (ReturnType.FULL, ReturnType.LINK):
            link_tag = single_result.find('a', class_="result__url")
            # raw link is of format "/url?q=REAL-LINK&sa=..."
            raw_link = self.base_url + link_tag.get('href')
            re_str = re.findall("uddg=(.+)", raw_link)[0]
            re_str = re_str.replace("%3A", ":")
            link = re_str.replace("%2F", "/")
            link = link.replace("%2D", "-")
            rdict["links"] = link

        if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
            desc = single_result.find(class_='result__snippet')
            rdict["descriptions"] = desc.text
        print(rdict)
        print(single_result)

        return rdict

    def headers(self):
        headers = {
            "Host": "duckduckgo.com",
            "User-Agent": utils.get_rand_user_agent(),
            "Accept-Encoding": "gzip",
            "DNT":"1",
            "Cache-Control": 'no-cache',
            "Connection": "keep-alive",
        }
        return headers
