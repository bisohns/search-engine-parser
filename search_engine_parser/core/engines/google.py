"""@desc 
		Parser for google search results
"""

from search_engine_parser.core.base import BaseSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError


class GoogleSearch(BaseSearch):
    """
    Searches Google for string
    """
    name = "Google"
    search_url = "https://www.google.com/search?client=ubuntu&q={query}&num=10&start={page}"
    summary = "\tNo need for further introductions. The search engine giant holds the first "\
            "place in search with a stunning difference of 65% from second in place Bing.\n"\
            "\tAccording to the latest netmarketshare report (November 2018) 73% of searches "\
            "were powered by Google and only 7.91% by Bing.\n\tGoogle is also dominating the "\
            "mobile/tablet search engine market share with 81%!"

    def parse_soup(self, soup):
        """
        Parses Google Search Soup for results
        """
        # find all class_='g' => each result
        return soup.find_all('div', class_='g')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="g">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        r = single_result.find('div', class_='r')
        link_tag = r.find('a')
        h3 = r.find('h3')
        desc = single_result.find('span', class_='st')
        ''' Get the text and link '''
        title = h3.text
        if not title:
            title = h3.find('div', class_='ellip').text

        raw_link = link_tag.get('href')

        desc = desc.text
        return title, raw_link, desc

