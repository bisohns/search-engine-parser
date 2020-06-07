"""@desc
		Parser for ask search results
"""
from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem


class Search(BaseSearch):
    """
    Searches Ask for string
    """
    name = "Ask"

    search_url = "https://www.ask.com/web?"

    summary = "\t Formerly known as Ask Jeeves, Ask.com receives approximately 0.42% of the search"\
        " share. ASK is based on a question/answer format where most questions are answered by "\
        "other users or are in the form of polls.\nIt also has the general search functionality "\
        "but the results returned lack quality compared to Google or even Bing and Yahoo."

    def get_params(self, query=None, page=None, offset=None, **kwargs):
        params = {}
        params["o"] = 0
        params["l"] = "dir"
        params["qo"] = "pagination"
        params["q"] = query
        params["qsrc"] = 998
        params["page"] = page
        return params

    def parse_soup(self, soup):
        """
        Parses Ask Search Soup for results
        """
        # find all class_='PartialSearchResults-item' => each result
        return soup.find_all('div', class_="PartialSearchResults-item")

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="PartialSearchResults-item">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """

        rdict = SearchItem()
        if return_type in (ReturnType.FULL, return_type.TITLE):
            rdict["titles"] = single_result.find('a').text

        if return_type in (ReturnType.FULL, return_type.TITLE):
            rdict["links"] = single_result.a["href"]

        if return_type in (ReturnType.FULL, return_type.TITLE):
            rdict["descriptions"] = single_result.find(
                'p', class_="PartialSearchResults-item-abstract").text

        return rdict
