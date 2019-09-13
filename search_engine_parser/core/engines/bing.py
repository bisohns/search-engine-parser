"""@desc 
		Parser for Bing search results
"""
from search_engine_parser.core.base import BaseSearch

class BingSearch(BaseSearch):
    """
    Searches Bing for string
    """
    name = "Bing"
    search_url = "https://www.bing.com/search?q={query}&count=10&offset=0&first={offset}&FORM=PERE"
    summary = "\tBing is Microsoft’s attempt to challenge Google in search, but despite their "\
            "efforts they still did not manage to convince users that their search engine can be"\
            " an alternative to Google.\n\tTheir search engine market share is constantly below "\
            "10%, even though Bing is the default search engine on Windows PCs."

    def parse_soup(self, soup):
        """
        Parses Bing for a search query.
        """
        # find all li tags
        return soup.find_all('li', class_='b_algo')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <li class="b_algo">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        h2 = single_result.find('h2')
        link_tag = h2.find('a')
        caption = single_result.find('div', class_='b_caption')
        desc = caption.find('p')
        ''' Get the text and link '''
        title = link_tag.text

        link = link_tag.get('href')

        desc = desc.text
        return title, link, desc

