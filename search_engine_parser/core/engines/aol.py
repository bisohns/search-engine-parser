"""@desc 
		Parser for AOL search results
"""
import re
from search_engine_parser.core.base import BaseSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError

class AolSearch(BaseSearch):
    """
    Searches Aol for string
    """
    name = "AOL"
    search_url = "https://search.aol.com/aol/search?q={query}"
    summary = "\t to be written"
    
    def search(self, soup):
        """
        Parses AOL for a search query
        """
        # find all divs
        return soup.find.all('div', class_='algo-sr')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return
        :param single_result: single result found in <div class="algo-sr">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        h2 = single_result.find('h2')
        link_tag = h2.find('a')
        caption = single_result.find('div', class_='compText aAbs')
        desc = caption.find('lh-16')
        ''' Get the text and link '''
        title = link_tag.text

        # raw link is of format "/url?q=REAL-LINK&sa=..."
        link = link_tag.get('href')

        desc = desc.text
        return title, link, desc
