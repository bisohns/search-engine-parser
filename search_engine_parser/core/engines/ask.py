"""@desc
		Parser for ask search results
"""
from search_engine_parser.core.base import BaseSearch, ReturnType


class AskSearch(BaseSearch):
    """
    Searches Ask for string
    """
    name = "Ask"

    search_url = "https://www.ask.com/web?o=0&l=dir&qo=pagination&q={query}&qsrc=998&page={page}"

    summary = "\t Formerly known as Ask Jeeves, Ask.com receives approximately 0.42% of the search"\
        " share. ASK is based on a question/answer format where most questions are answered by "\
        "other users or are in the form of polls.\nIt also has the general search functionality "\
        "but the results returned lack quality compared to Google or even Bing and Yahoo."

    def parse_soup(self, soup):
        """
        Parses Ask Search Soup for results
        """
        # find all class_='PartialSearchResults-item' => each result
        return soup.find_all('div', class_="PartialSearchResults-item")

    def parse_single_result(self, single_result, return_type=ReturnType.FULL):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="PartialSearchResults-item">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """

        rdict = {}
        if return_type in (ReturnType.FULL, return_type.TITLE):
            rdict["titles"] = single_result.find('a').text

        if return_type in (ReturnType.FULL, return_type.TITLE):
            rdict["links"] = single_result.a["href"]

        if return_type in (ReturnType.FULL, return_type.TITLE):
            rdict["descriptions"] = single_result.find(
                'p', class_="PartialSearchResults-item-abstract").text


        return rdict
