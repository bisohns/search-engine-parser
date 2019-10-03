"""@desc
		Parser for AOL search results
"""
from search_engine_parser.core.base import BaseSearch


class StackOverflowSearch(BaseSearch):
    """
    Searches StackOverflow for string
    """
    name = "StackOverflow"
    base_url = "https://stackoverflow.com"
    search_url = base_url + "/search?q={query}&page={page}&pagesize=15"
    summary = "\tStack Overflow is a question and answer site for professional and enthusiast "\
              "programmers.\n\tIt is a privately held website, the flagship site of the Stack "\
              "Exchange Network, created in 2008 by Jeff Atwood and Joel Spolsky.\n\tIt features "
              "questions and answers on a wide range of topics in computer programming. It was "\
              "created to be a more open alternative to earlier question and answer sites "\
              "such as Experts-Exchange"

    def parse_soup(self, soup):
        """
        Parses StackOverflow for a search query
        """
        # find all divs
        return soup.find_all('div', class_='summary')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return
        
        :param single_result: single result found in <div class="summary">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        h3 = single_result.find('h3') #pylint: disable=invalid-name
        link_tag = h3.find('a')
        caption = single_result.find('div', class_='excerpt')
        # Get the text and link
        title = link_tag.text

        ref_link = link_tag.get('href')
        link = self.base_url + ref_link

        desc = caption.text
        rdict = {
            "titles": title,
            "links": link,
            "descriptions": desc,
        }
        return rdict
