"""@desc
		Parser for google search results
"""

from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem


class Search(BaseSearch):
    """
    Searches Google for string
    """
    name = "Google"
    search_url = "https://www.google.com/search?"
    summary = "\tNo need for further introductions. The search engine giant holds the first "\
        "place in search with a stunning difference of 65% from second in place Bing.\n"\
        "\tAccording to the latest netmarketshare report (November 2018) 73% of searches "\
        "were powered by Google and only 7.91% by Bing.\n\tGoogle is also dominating the "\
        "mobile/tablet search engine market share with 81%!"

    def get_params(self, query=None, offset=None, page=None, **kwargs):
        params = {}
        params["num"] = 10
        params["start"] = page
        params["q"] = query
        params["client"] = "ubuntu"
        return params

    def parse_soup(self, soup):
        """
        Parses Google Search Soup for results
        """
        # find all class_='g' => each result
        return soup.find_all('div', class_='g')

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="g">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        results = SearchItem()
        r_elem = single_result.find('div', class_='r')

        # Get the text and link
        if return_type in (ReturnType.FULL, return_type.TITLE):
            h3_tag = r_elem.find('h3')
            title = h3_tag.text
            if not title:
                title = h3_tag.find('div', class_='ellip').text
            results['titles'] = title

        if return_type in (ReturnType.FULL, ReturnType.LINK):
            link_tag = r_elem.find('a')
            raw_link = link_tag.get('href')
            results['links'] = raw_link

        if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
            desc = single_result.find('span', class_='st')
            desc = desc.text
            results['descriptions'] = desc

        return results
