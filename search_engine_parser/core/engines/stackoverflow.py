"""@desc
		Parser for AOL search results
"""
from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem


class Search(BaseSearch):
    """
    Searches StackOverflow for string
    """
    name = "StackOverflow"
    base_url = "https://stackoverflow.com"
    search_url = base_url + "/search?"
    summary = "\tStack Overflow is a question and answer site for professional and enthusiast "\
              "programmers.\n\tIt is a privately held website, the flagship site of the Stack "\
              "Exchange Network, created in 2008 by Jeff Atwood and Joel Spolsky.\n\tIt features "\
              "questions and answers on a wide range of topics in computer programming. It was "\
              "created to be a more open alternative to earlier question and answer sites "\
              "such as Experts-Exchange"

    def get_params(self, query=None, offset=None, page=None, **kwargs):
        params = {}
        params["page"] = page
        params["q"] = query
        params["pagesize"] = 15
        return params

    def parse_soup(self, soup):
        """
        Parses StackOverflow for a search query
        """
        # find all divs
        return soup.find_all('div', class_='summary')

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="summary">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        rdict = SearchItem()
        h3 = single_result.find('h3')  # pylint: disable=invalid-name
        link_tag = h3.find('a')
        if return_type in (ReturnType.FULL, return_type.TITLE):
            # Get the text and link
            rdict["titles"] = link_tag.text

        if return_type in (ReturnType.FULL, return_type.LINK):
            ref_link = link_tag.get('href')
            link = self.base_url + ref_link
            rdict["links"] = link

        if return_type in (ReturnType.FULL, return_type.DESCRIPTION):
            caption = single_result.find('div', class_='excerpt')
            rdict["descriptions"] = caption.text
        return rdict
