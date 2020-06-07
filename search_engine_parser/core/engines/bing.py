"""@desc
		Parser for Bing search results
"""
from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem


class Search(BaseSearch):
    """
    Searches Bing for string
    """
    name = "Bing"
    search_url = "https://www.bing.com/search?"
    summary = "\tBing is Microsoft’s attempt to challenge Google in search, but despite their "\
        "efforts they still did not manage to convince users that their search engine can be"\
        " an alternative to Google.\n\tTheir search engine market share is constantly below "\
        "10%, even though Bing is the default search engine on Windows PCs."

    def get_params(self, query=None, page=None, offset=None, **kwargs):
        params = {}
        params["q"] = query
        params["offset"] = 0
        params["first"] = offset
        params["count"] = 10
        params["FORM"] = "PERE"
        return params

    def parse_soup(self, soup):
        """
        Parses Bing for a search query.
        """
        # find all li tags
        return soup.find_all('li', class_='b_algo')

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in <li class="b_algo">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        rdict = SearchItem()
        h2_tag = single_result.find('h2')
        link_tag = h2_tag.find('a')

        if return_type in (ReturnType.FULL, return_type.TITLE):
            rdict["titles"] = link_tag.text

        if return_type in (ReturnType.FULL, return_type.LINK):
            link = link_tag.get('href')
            rdict["links"] = link

        if return_type in (ReturnType.FULL, return_type.DESCRIPTION):
            caption = single_result.find('div', class_='b_caption')
            desc = caption.find('p')
            rdict["descriptions"] = desc.text

        return rdict
