"""@desc
		Parser for AOL search results
"""
from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem


class Search(BaseSearch):
    """
    Searches Aol for string
    """
    name = "AOL"
    search_url = "https://search.aol.com/aol/search?"
    summary = "\t According to netmarketshare, the old time famous AOL is still in the top 10 "\
        "search engines with a market share that is close to 0.06%. "\
        "The AOL network includes many popular web sites like engadget.com, techchrunch.com and "\
        "the huffingtonpost.com. \nOn June 23, 2015, AOL was acquired by Verizon Communications."

    def parse_soup(self, soup):
        """
        Parses AOL for a search query
        """
        # find all divs
        return soup.find_all('div', class_='algo-sr')

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="algo-sr">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        rdict = SearchItem()
        h3_tag = single_result.find('h3')
        link_tag = h3_tag.find('a')
        if return_type in (ReturnType.FULL, return_type.TITLE):
            # Get the text and link
            rdict["titles"] = link_tag.text

        if return_type in (ReturnType.FULL, ReturnType.LINK):
            rdict["links"] = link_tag.get("href")

        if return_type in (ReturnType.FULL, return_type.DESCRIPTION):
            caption = single_result.find('div', class_='compText aAbs')
            desc = caption.find('p', class_='lh-16')
            rdict["descriptions"] = desc.text

        return rdict
