"""@desc
		Parser for google news search results
"""

from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem


class Search(BaseSearch):
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

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="g">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link, description, imge link, news source, date of single result
        :rtype: dict
        """
        rdict = SearchItem()

        if return_type in (ReturnType.FULL, return_type.TITLE):
            title_tag = single_result.find('h3')
            title = title_tag.text
            rdict["titles"] = title

        if return_type in (ReturnType.FULL, ReturnType.LINK):
            link_tag = single_result.find('a')
            rdict["links"] = link_tag.get('href')

        if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
            desc_tag = single_result.find('div', class_='st')
            rdict["descriptions"] = desc_tag.text

        if return_type in (ReturnType.FULL,):
            img_tag = single_result.find('img', class_='th')
            news_source_tag = single_result.find('span', class_='e8fRJf')
            date_tag = single_result.find('span', class_='f')

            rdict["image_url"] = img_tag.get('src')
            rdict["news_source"] = news_source_tag.text
            rdict["date"] = date_tag.text
        return rdict
