"""@desc
		Parser for google news search results
"""

from search_engine_parser.core.base import BaseSearch


class GoogleNewsSearch(BaseSearch):
    """
    Searches Google News for string
    """
    name = "GoogleNews"
    search_url = "https://www.google.com/search?"
    summary = "\tGoogle News is a news aggregator app developed by Google. It presents a "\
        "continuous, customizable flow of articles organized from thousands of publishers "\
        "and magazines. Google News is available as an app on Android, iOS, and the Web. "\
        "Google released a beta version in September 2002 and the official app in January 2006."

    def get_params(self, query=None, offset=None, page=None, **kwargs):
        params = {}
        params["num"] = 10
        params["start"] = page
        params["q"] = query
        params["client"] = "ubuntu"
        params["tbm"] = "nws"
        return params

    def parse_soup(self, soup):
        """
        Parses Google News Search Soup for results
        """
        # find all class_='g' => each result
        return soup.find_all('div', class_='g')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="g">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link, description, imge link, news source, date of single result
        :rtype: dict
        """

        link_tag = single_result.find('a')
        title_tag = single_result.find('h3')
        desc_tag = single_result.find('div', class_='st')
        img_tag = single_result.find('img', class_='th')
        news_source_tag = single_result.find('span', class_='e8fRJf')
        date_tag = single_result.find('span', class_='f')
        
        title = title_tag.text
        raw_link = link_tag.get('href')
        desc = desc_tag.text
        img = img_tag.get('src')
        news_source = news_source_tag.text
        date = date_tag.text 

        rdict = {
            "titles": title,
            "links": raw_link,
            "descriptions": desc,
            "image_url" : img,
            "news_source" : news_source,
            "date" : date
        }
        return rdict
