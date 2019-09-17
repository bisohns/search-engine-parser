"""@desc 
		Parser for GitHub search results
"""
from search_engine_parser.core.base import BaseSearch

class GitHubSearch(BaseSearch):
    """
    Searches GitHub for string
    """
    name = "GitHub"
    base_url = "https://github.com"
    search_url = base_url + "/search?q={query}&p={page}"
    summary = "\tGitHub is an American company that provides hosting for software development version control using Git. "\
        " It is a subsidiary of Microsoft, which acquired the company in 2018 for $7.5 billion." \
        "\n\tIt offers all of the distributed version control and source code management (SCM) functionality of Git as well as adding its own features."\
        "\n\tAs of May 2019, GitHub reports having over 37 million users and more than 100 million repositories (including at least 28 million public repositories),"\
        "making it the largest host of source code in the world."

    def parse_soup(self, soup):
        """
        Parses GitHub for a search query.
        """
        # find all li tags
        return soup.find_all('li', class_='repo-list-item')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <li class="repo-list-item">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        h3 = single_result.find('h3')
        link_tag = h3.find('a')
        ''' Get the text and link '''
        title = link_tag.text

        ref_link = link_tag.get('href')
        link = self.base_url + ref_link

        desc = single_result.find('p', class_="col-12")
        stars_and_lang_div = single_result.find('div', class_='flex-shrink-0')
        lang = stars_and_lang_div.find('span', itemprop="programmingLanguage").text
        stars = stars_and_lang_div.find('a', class_='muted-link').text.strip()

        desc = desc.text
        title = f"{title}\t {lang}\t Stars-{stars}"
        return title, link, desc

