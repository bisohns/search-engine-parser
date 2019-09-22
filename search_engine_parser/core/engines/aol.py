"""@desc
		Parser for AOL search results
"""
from search_engine_parser.core.base import BaseSearch


class AolSearch(BaseSearch):
    """
    Searches Aol for string
    """
    name = "AOL"
    search_url = "https://search.aol.com/aol/search?q={query}&page={page}"
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

    def parse_single_result(self, single_result):
        """
        Parses the source code to return
        :param single_result: single result found in <div class="algo-sr">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        h3 = single_result.find('h3')
        link_tag = h3.find('a')
        caption = single_result.find('div', class_='compText aAbs')
        desc = caption.find('p', class_='lh-16')
        # Get the text and link
        title = link_tag.text

        link = link_tag.get('href')

        desc = desc.text
        rdict = dict()
        if title and link and desc:
            rdict = {
                "titles": title,
                "links": link,
                "descriptions": desc,
            }
        return rdict
