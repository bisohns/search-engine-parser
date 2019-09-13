"""@desc 
		Parser for AOL search results
"""
import re
from search_engine_parser.core.base import BaseSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError

class StackOverflowSearch(BaseSearch):
    """
    Searches Aol for string
    """
    name = "StackOverflow"
    base_url = "https://stackoverflow.com"
    search_url = base_url + "/search?q={query}&page={page}&pagesize=15"
    summary = "\t Stack Overflow is a question and answer site for professional and enthusiast programmers. "\
	      "It is a privately held website, the flagship site of the Stack Exchange Network, created in 2008 by Jeff Atwood and Joel Spolsky. "\
	      "As of January 2019 Stack Overflow has over 10 million registered users, and it exceeded 16 million questions in mid 2018."   
    
    def parse_soup(self, soup):
        """
        Parses StackOverflow for a search query
        """
        # find all divs
        return soup.find_all('div', class_='summary')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return
        :param single_result: single result found in <div class="summary">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        h3 = single_result.find('h3')
        link_tag = h3.find('a')
        caption = single_result.find('div', class_='excerpt')
        ''' Get the text and link '''
        title = link_tag.text

        ref_link = link_tag.get('href')
        link = self.base_url + ref_link

        desc = caption.text
        return title, link, desc
