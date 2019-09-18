"""@desc 
		Parser for Yahoo search results
"""

from search_engine_parser.core.base import BaseSearch


class YahooSearch(BaseSearch):
    """
    Searches Yahoo for string
    """
    name = "Yahoo"
    search_url = "https://search.yahoo.com/search?p={query}&b={offset}"
    summary = "\tYahoo is one the most popular email providers and holds the fourth place in "\
            "search with 3.90% market share.\n\tFrom October 2011 to October 2015, Yahoo search "\
            "was powered exclusively by Bing. \n\tSince October 2015 Yahoo agreed with Google to "\
            "provide search-related services and since then the results of Yahoo are powered both "\
            "by Google and Bing. \n\tYahoo is also the default search engine for Firefox browsers "\
            "in the United States (since 2014)."

    def parse_soup(self, soup):
        """
        Parses Yahoo for a search query
        """
        # find all divs
        return soup.find_all('div', class_='Sr')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="Sr">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        h3 = single_result.find('h3', class_='title')
        link_tag = h3.find('a')
        desc = single_result.find('p', class_='lh-16')
        
        title = h3.text

        link = link_tag.get('href')

        desc = desc.text
        return title, link, desc

