"""@desc
		Parser for MyAnimeList search results
"""

import math
import sys

from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem


class Search(BaseSearch):
    """
    Searches MyAnimeList for string
    """
    name = "MyAnimeList"

    search_url = "https://myanimelist.net/anime.php?"
    summary = "\tMyAnimeList, often abbreviated as MAL, is an anime and manga social"\
        "networking and social cataloging application website."\
        "\n\tThe site provides its users with a list-like system to organize"\
        "and score anime and manga.\n\tIt facilitates finding users who share"\
        "similar tastes and provides a large database on anime and manga.\n\tThe"\
        "site claims to have 4.4 million anime and 775,000 manga entries."\
        "\n\tIn 2015, the site received over 120 million visitors a month."

    def get_params(self, query=None, page=None, offset=None, **kwargs):
        params = {}
        params["show"] = (math.ceil(page / 5) - 1) * 50
        params["q"] = query
        return params

    def parse_soup(self, soup):
        """
        Parses MyAnimeList for a search query
        """

        # The data is stored in table so find all table rows
        # The first row is table header
        res = soup.find('div', class_='js-categories-seasonal js-block-list list')
        if res:
            return res.find_all('tr')[1:]

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in div with a numeric id
        :type single_result: `bs4.element.Tag`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        rdict = SearchItem()
        link_tag = single_result.find('a', class_='fw-b')

        if return_type in (ReturnType.FULL, return_type.TITLE):
            title = link_tag.find('strong').text
            rdict["titles"] = title

        if return_type in (ReturnType.FULL, ReturnType.LINK):
            rdict["links"] = link_tag.get('href')

        if return_type in (ReturnType.FULL, return_type.DESCRIPTION):
            desc = single_result.find('div', class_='pt4').text.strip()
            rdict["descriptions"] = desc

        if return_type == ReturnType.FULL:
            data = list(single_result.find_all('td', class_='ac'))
            animetype = data[0].text.strip()
            episodes = data[1].text.strip()
            score = data[2].text.strip()

            rdict.update({
                "episode_count": episodes,
                "animetypes": animetype,
                "ratings": score
            })
        return rdict
