"""@desc
		Parser for google search results
"""

from search_engine_parser.core.base import BaseSearch


class GoogleSearch(BaseSearch):
    """
    Searches Google for string
    """
    name = "Google"
    search_url = "https://www.google.com/search?client=ubuntu&q={query}&num=10&start={page}"
    summary = "\tNo need for further introductions. The search engine giant holds the first "\
        "place in search with a stunning difference of 65% from second in place Bing.\n"\
        "\tAccording to the latest netmarketshare report (November 2018) 73% of searches "\
        "were powered by Google and only 7.91% by Bing.\n\tGoogle is also dominating the "\
        "mobile/tablet search engine market share with 81%!"

    def parse_soup(self, soup):
        """
        Parses Google Search Soup for results
        """
        # find all class_='g' => each result
        return soup.find_all('div', class_='g')

    # Elements is a 2d array consting of names, html tags and classes
    # Elements = [['link_tags', 'a', 'r'], ['r_elem', 'div', 'st'] ... ]
    def parse_single_result(self, single_result, element):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="g">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
	results = {}
	for i in elements:
	    # Creates a variable
	    vars[i[0]] = single_result.find(i[0], i[1])
		       
	    #r_elem = single_result.find('div', class_='r')
            #link_tag = r_elem.find('a')
            #h3_tag = r_elem.find('h3')
            #desc = single_result.find('span', class_='st')
        
	# Get the text and link
	if 'h3_tag' in vars:
            title = h3_tag.text
            if not title:
                title = h3_tag.find('div', class_='ellip').text
	    results['titles'] = title
	
        if 'link_tag' in vars:
            raw_link = link_tag.get('href')
	    results['links'] = raw_link

	if 'desc' in vars:
            desc = desc.text
	    results['descriptions'] = desc
		
        return results
