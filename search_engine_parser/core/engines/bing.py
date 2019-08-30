"""@desc 
		Parser for Bing search results
"""
from search_engine_parser.core.base import BaseSearch

class BingSearch(BaseSearch):
    """
    Searches Bing for string
    """
    def search(self, query, page=1):
        """
        Parses Bing for a search query.

        :param query: Search query sentence or term
        :type query: string
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        soup = BingSearch.get_soup(query, engine="Bing", page=page)
        # find all li tags
        results = soup.find_all('li', class_='b_algo')
        if not results:
            raise ValueError("The result parsing was unsuccessful, flagged as unusual traffic")
        search_results = self.parse_result(results)
        if len(search_results) > 0:
            print("Got Results")
        return search_results 

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

        # raw link is of format "/url?q=REAL-LINK&sa=..."
        link = link_tag.get('href')

        desc = desc.text
        return title, link, desc

