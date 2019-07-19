"""@desc 
		Individual engines that inherit from base engine

 	@author 
 		Domnan Diretnan
 		Artificial Intelligence Enthusiast & Software Engineer.
 		Email: diretnandomnan@gmail.com
 		Github: https://github.com/deven96
 		GitLab: https://gitlab.com/Deven96

 	@project
 		@create date 2019-02-01 22:21:41
 		@modify date 2019-02-01 22:21:41

	@license
		MIT License
		Copyright (c) 2018. Domnan Diretnan. All rights reserved

 """
"""@desc 
		Parser for google search results

 	@author 
 		Domnan Diretnan
 		Artificial Intelligence Enthusiast & Software Engineer.
 		Email: diretnandomnan@gmail.com
 		Github: https://github.com/deven96
 		GitLab: https://gitlab.com/Deven96

 	@project
 		@create date 2019-01-26 23:14:22
 		@modify date 2019-01-26 23:14:22

	@license
		MIT License
		Copyright (c) 2018. Domnan Diretnan. All rights reserved

 """

from base import BaseSearch


class GoogleSearch(BaseSearch):
    """
    Searches Google for string
    """
    def search(self, query, page=1):
        """
        Parses Google for a search query.

        :param query: Search query sentence or term
        :type query: string
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        soup = GoogleSearch.get_soup(query, engine="Google", page=page)
        # # find all class_='g' => each result
        results = soup.find_all('div', class_='g')
        if not results:
            raise ValueError("The result parsing was unsuccessful, flagged as unusual traffic")
        search_results = self.parse_result(results)
        if len(search_results) > 0:
            print("Got Results")
        return search_results

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="g">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        r = single_result.find('div', class_='r')
        link_tag = r.find('a')
        h3 = r.find('h3')
        desc = single_result.find('span', class_='st')
        ''' Get the text and link '''
        title = h3.text

        # raw link is of format "/url?q=REAL-LINK&sa=..."
        raw_link = link_tag.get('href')

        desc = desc.text
        return title, raw_link, desc

class YahooSearch(BaseSearch):
    """
    Searches Yahoo for string
    """
    def search(self, query, page=1):
        """
        Parses Yahoo for a search query.

        :param query: Search query sentence or term
        :type query: string
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        soup = YahooSearch.get_soup(query, engine="Yahoo", page=page)
        # find all divs
        results = soup.find_all('div', class_='Sr')
        if not results:
            raise ValueError("The result parsing was unsuccessful, flagged as unusual traffic")
        search_results = self.parse_result(results)
        if len(search_results) > 0:
            print("Got Results")
        return search_results 

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="Sr">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        h3 = single_result.find('h3', class_='title')
        link_tag = h3.find('a')
        desc = single_result.find('p', class_='lh-16')
        ''' Get the text and link '''
        title = h3.text

        # raw link is of format "/url?q=REAL-LINK&sa=..."
        link = link_tag.get('href')

        desc = desc.text
        return title, link, desc

class BingSearch(BaseSearch):
    """
    Searches Bing for string
    """
    def search(self, query, page=1):
        """
        Parses Bing for a search query.

        :param query: Search query sentence or term
        :type query: string
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :return: dictionary. Containing titles, links, netlocs and descriptions.
        """
        soup = BingSearch.get_soup(query, engine="Bing", page=page)
        # find all divs
        results = soup.find_all('li', class_='b_algo')
        if not results:
            raise ValueError("The result parsing was unsuccessful, flagged as unusual traffic")
        search_results = self.parse_result(results)
        if len(search_results) > 0:
            print("Got Results")
        return search_results 

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="Sr">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        h2 = single_result.find('h2')
        link_tag = h2.find('a')
        caption = single_result.find('div', class_='b_caption')
        desc = caption.find('p')
        ''' Get the text and link '''
        title = link_tag.text

        # raw link is of format "/url?q=REAL-LINK&sa=..."
        link = link_tag.get('href')

        desc = desc.text
        return title, link, desc

if __name__ == '__main__':
    print("starting")
    search_args = ('preaching to the choir', 1)
    gsearch = GoogleSearch()
    print("Initialized google scraper")
    ysearch = YahooSearch()
    print("Initialized yahoo scraper")
    bsearch = BingSearch()
    print("Initialized bing scraper")
    gresults = gsearch.search(*search_args)
    yresults = ysearch.search(*search_args)
    bresults = bsearch.search(*search_args)
    print(yresults["titles"][1])
    print(gresults["titles"][1])
    print(bresults["titles"][1])

