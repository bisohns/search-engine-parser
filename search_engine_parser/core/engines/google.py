"""@desc 
		Parser for google search results
"""

from search_engine_parser.core.base import BaseSearch


class GoogleSearch(BaseSearch):
    """
    Searches Google for string
    """
    def search(self, query, page=1):
        """
        Parses Google for a search query.

        :param query: Search query sentence or term
        :type query: string
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        soup = GoogleSearch.get_soup(query, engine="Google", page=page)
        # # find all class_='g' => each result
        results = soup.find_all('div', class_='g')
        if not results:
            raise ValueError("The result parsing was unsuccessful, flagged as unusual traffic")
        search_results = self.parse_result(results)
        if len(search_results) > 0:
            print("Got Results")
        return search_results

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

        # raw link is of format "/url?q=REAL-LINK&sa=..."
        raw_link = link_tag.get('href')

        desc = desc.text
        return title, raw_link, desc

