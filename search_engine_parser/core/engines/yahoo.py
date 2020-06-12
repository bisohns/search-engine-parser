"""@desc
		Parser for Yahoo search results
"""
import re

from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem


class Search(BaseSearch):
    """
    Searches Yahoo for string
    """
    name = "Yahoo"
    search_url = "https://search.yahoo.com/search?"
    summary = "\tYahoo is one the most popular email providers and holds the fourth place in "\
        "search with 3.90% market share.\n\tFrom October 2011 to October 2015, Yahoo search "\
        "was powered exclusively by Bing. \n\tSince October 2015 Yahoo agreed with Google to "\
        "provide search-related services and since then the results of Yahoo are powered both "\
        "by Google and Bing. \n\tYahoo is also the default search engine for Firefox browsers "\
        "in the United States (since 2014)."

    def get_params(self, query=None, page=None, offset=None, **kwargs):
        params = {}
        params["p"] = query
        params["b"] = offset
        return params

    def parse_soup(self, soup):
        """
        Parses Yahoo for a search query
        """
        # find all divs
        return soup.find_all('div', class_='Sr')

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="Sr">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        rdict = SearchItem()
        h3_tag = single_result.find('h3', class_='title')

        if return_type in (ReturnType.FULL, return_type.TITLE):
            title = h3_tag.text
            rdict["titles"] = title

        if return_type in (ReturnType.FULL, ReturnType.LINK):
            link_tag = h3_tag.find('a')
            raw_link = link_tag.get('href')
            re_str = re.findall("/RU=(.+)/RK", raw_link)[0]
            re_str = re_str.replace("%3a", ":")
            link = re_str.replace("%2f", "/")
            rdict["links"] = link

        if return_type in (ReturnType.FULL, return_type.DESCRIPTION):
            desc = single_result.find('p', class_='fz-ms')
            rdict["descriptions"] = desc.text

        return rdict
