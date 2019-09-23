"""@desc 
		Parser for ask search results
"""
from search_engine_parser.core.base import BaseSearch


class AskSearch(BaseSearch):
    """
    Searches Ask for string
    """
    name = "Ask"
    
    search_url = "https://www.ask.com/web?o=0&l=dir&qo=pagination&q={query}&qsrc=998&page={page}"
    
    summary = "\t Formerly known as Ask Jeeves, Ask.com receives approximately 0.42% of the search share."\
        "ASK is based on a question/answer format where most questions are answered by other users"\
        "or are in the form of polls.\nIt also has the general search functionality but the results"\
        "returned lack quality compared to Google or even Bing and Yahoo."

    def parse_soup(self, soup):
        """
        Parses Ask Search Soup for results
        """
        # find all class_='PartialSearchResults-item' => each result
        return soup.find_all('div', class_="PartialSearchResults-item")        

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="PartialSearchResults-item">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        
        title = single_result.find('a').text
        link = single_result.a["href"]
        desc = single_result.find('p', class_="PartialSearchResults-item-abstract").text	
        search_results = {
            "titles": title,
            "links": link,
            "descriptions": desc,
        }
	
        return search_results
