"""@desc
		Parser for google search results
"""
import sys
from urllib.parse import (
    urljoin,
    parse_qs,
    unquote
)
import urllib.parse as urlparse

from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem


EXTRA_PARAMS = ('hl', 'tbs')


class Search(BaseSearch):
    """
    Searches Google for string
    """
    name = "Google"
    base_url = "https://www.google.com/"
    summary = "\tNo need for further introductions. The search engine giant holds the first "\
        "place in search with a stunning difference of 65% from second in place Bing.\n"\
        "\tAccording to the latest netmarketshare report (November 2018) 73% of searches "\
        "were powered by Google and only 7.91% by Bing.\n\tGoogle is also dominating the "\
        "mobile/tablet search engine market share with 81%!"

    def __init__(self):
        super().__init__()
        self.search_url = urljoin(self.base_url, "search")

    def get_params(self, query=None, offset=None, page=None, **kwargs):
        params = {}
        params["start"] = (page-1) * 10
        params["q"] = query
        params["gbv"] = 1
        # additional parameters will be considered
        for param in EXTRA_PARAMS:
            if kwargs.get(param):
                params[param] = kwargs[param]
        return params

    def parse_url(self, url):
        return self.clean_url(urljoin(self.base_url, url))

    def parse_soup(self, soup):
        """
        Parses Google Search Soup for results
        """
        # find all class_='g' => each result
        return soup.find_all('div', class_="Gx5Zad fP1Qef xpd EtOod pkphOe")

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="g">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        # Some unneeded details shown such as suggestions should be ignore
        if (single_result.find("h2", class_="wITvVb") and single_result.find("div", class_="LKSyXe"))\
                or single_result.find("div", class_="X7NTVe"):
            return

        results = SearchItem()
        els = single_result.find_all('div', class_='kCrYT')
        if len(els) < 2:
            return

        # First div contains title and url
        r_elem = els[0]

        # Get the text and link
        if return_type in (ReturnType.FULL, ReturnType.TITLE):
            link_tag = r_elem.find('a')
            if link_tag:
                title = link_tag.find('h3').text
            else:
                r_elem = els[1]
                title = r_elem.find('div', class_='BNeawe').text
            results['titles'] = title

        if return_type in (ReturnType.FULL, ReturnType.LINK):
            link_tag = r_elem.find('a')
            if link_tag:
                raw_link = link_tag.get('href')
                raw_url = urljoin(self.base_url, raw_link)
                results['raw_urls'] = raw_url
                results['links'] = self.clean_url(raw_url)

        if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
            # Second Div contains Description
            desc_tag = els[1]
            if return_type in (ReturnType.FULL, ReturnType.LINK) and not results.get('links'):
                link_tag = desc_tag.find('a')
                if link_tag:
                    desc_tag = els[0]
                    raw_link = link_tag.get('href')
                    raw_url = urljoin(self.base_url, raw_link)
                    results['raw_urls'] = raw_url
                    results['links'] = self.clean_url(raw_url)
            desc = desc_tag.text
            results['descriptions'] = desc
        return results

    def clean_url(self, url):
        """
        Extract clean URL from the SERP URL.

        >clean_url('https://www.google.com/url?q=https://english.stackexchange.com/questions/140710/what-is-the-opposite-of-preaching-to-the-choir&sa=U&ved=2ahUKEwi31MGyzvnuAhXyyDgGHXXACOYQFnoECAkQAg&usg=AOvVaw1GdXON-JIWGu-dGjHfgljl')
        https://english.stackexchange.com/questions/140710/what-is-the-opposite-of-preaching-to-the-choir
        """
        parsed = urlparse.urlparse(url)
        url_qs = parse_qs(parsed.query)
        if 'q' in url_qs:
            return unquote(url_qs['q'][0])
        elif 'url' in url_qs:
            return unquote(url_qs['url'][0])
        # Add more cases here.
        return url
