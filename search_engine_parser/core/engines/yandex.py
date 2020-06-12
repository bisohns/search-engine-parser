"""@desc
		Parser for Yandex search results
"""

from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem


class Search(BaseSearch):
    """
    Searches Yandex for string
    """
    name = "Yandex"
    search_url = "https://yandex.com/search/?"
    summary = "\tYandex is the largest technology company in Russia and the"\
        " largest search engine on the internet in Russian"\
        ", with a market share of over 52%."\
        "\n\tThe Yandex.ru home page is the 4th most popular website in Russia."\
        "\n\tIt also has the largest market share of any search engine in the Commonwealth"\
        " of Independent States and is the 5th largest search engine worldwide"\
        " after Google, Baidu, Bing, and Yahoo!"

    def get_params(self, query=None, page=None, offset=None, **kwargs):
        params = {}
        params["text"] = query
        params["p"] = offset
        return params

    def parse_soup(self, soup):
        """
        Parses Yandex for a search query
        """
        return soup.find_all('li', class_="serp-item")

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in <li class="serp-item">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        rdict = SearchItem()
        h3_tag = single_result.find('div', class_="organic__url-text")

        if return_type in (ReturnType.FULL, return_type.TITLE):
            # Get the text and link
            title = h3_tag.text
            # Handle read more type texts
            index = title.find("Read more")
            if index >= 0:
                title = title[0:int(index)]
            rdict["titles"] = title

        if return_type in (ReturnType.FULL, ReturnType.LINK):
            link_tag = single_result.find('a')
            link = link_tag.get('href')
            rdict["links"] = link

        if return_type in (ReturnType.FULL, return_type.DESCRIPTION):
            desc = single_result.find('div', class_="organic__content-wrapper")
            desc = desc.text
            rdict["descriptions"] = desc
        return rdict
