"""@desc
		Parser for GitHub search results
"""
from search_engine_parser.core.base import BaseSearch
from search_engine_parser.core.exceptions import IncorrectKeyWord


class GitHubSearch(BaseSearch):
    """
    Searches GitHub for string
    """
    name = "GitHub"
    base_url = "https://github.com"
    search_url = base_url + "/search?q={query}&p={page}&type={type_}"
    summary = "\tGitHub is an American company that provides hosting for software development "\
        "version control using Git. It is a subsidiary of Microsoft, which acquired the company "\
        "in 2018 for $7.5 billion.\n\tIt offers all of the distributed version control and source"\
        " code management (SCM) functionality of Git as well as adding its own features."\
        "\n\tAs of May 2019, GitHub reports having over 37 million users and more than 100 million"\
        " repositories (including at least 28 million public repositories), making it the largest "\
        "host of source code in the world."
    def parse_soup(self, soup):
        """
        Parses GitHub for a search query.
        """
        allowed_types = (
            None,
            "Repositories",
            "Wikis",
            "Users",
            "Topics",
            "Marketplace",
            "Packages",
            "Issues",
            "Commits",
            "Code")
        self.type = self.keywords.get("type", None)
        if self.type not in allowed_types:
            raise IncorrectKeyWord("No type <{type_}> exists".format(type_=self.type))
        # find all li tags
        if self.type in (None, "Repositories", "Packages"):
            return soup.find_all('li', class_='repo-list-item')
        # find all user divs
        elif self.type == "Users":
            return soup.find_all('div', class_='user-list-item')
        elif self.type == "Wikis":
            return soup.find_all('div', class_='wiki-list-item')
        elif self.type == "Topics":
            return soup.find_all('div', class_='topic-list-item')
        elif self.type in ("Marketplace", "Issues"):
            return soup.find_all('div', class_='issue-list-item')
        elif self.type == "Commits":
            return soup.find_all('div', class_='commits-list-item')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in container element
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        if self.type in (None, "Repositories"):
            h3 = single_result.find('h3') #pylint: disable=invalid-name
            link_tag = h3.find('a')
            # Get the text and link
            title = link_tag.text

            ref_link = link_tag.get('href')
            link = self.base_url + ref_link

            desc = single_result.find('p', class_="col-12")
            stars_and_lang_div = single_result.find('div', class_='flex-shrink-0')
            lang = stars_and_lang_div.find(
                'span', itemprop="programmingLanguage").text
            stars = stars_and_lang_div.find('a', class_='muted-link').text.strip()

            desc = desc.text
            return {
                "titles": title,
                "links": link,
                "descriptions": desc,
                "stars": stars,
                "languages": lang,
            }
        if self.type == "Users":
            title_tag = single_result.find('a', class_=None)
            title = title_tag.text
            ref_link = title_tag.get('href')
            link = self.base_url + ref_link
            desc_tag = single_result.find('p', class_='f5 mt-2')
            location_tag = single_result.find('li', class_='mt-1')
            desc = None
            location = None
            if desc_tag:
                desc = desc_tag.text.strip(' \n')
            if location_tag:
                location = location_tag.text.strip(' \n')
            return {
                "titles": title,
                "links": link,
                "descriptions": desc,
                "locations": location,
            }
        if self.type == "Wikis":
            repository = single_result.find('a', class_='h5').text
            title_tag = single_result.find('a', class_=None)
            title = title_tag.get('title')
            ref_link = title_tag.get('href')
            link = self.base_url + ref_link
            desc = single_result.find('p', class_=None).text
            last_updated = single_result.find('div', class_='updated-at').find('relative-time').text
            return {
                "titles": title,
                "links": link,
                "descriptions": desc,
                "repositories": repository,
                "last_updated": last_updated,
            }
        if self.type == "Topics":
            title_div = single_result.find('h3')
            title_tag = title_div.find('a', class_=None)
            title = title_tag.text
            ref_link = title_tag.get('href')
            desc = None
            desc_tag = single_result.find('p', class_=None)
            if desc_tag:
                desc = desc_tag.text
            link = self.base_url + ref_link
            return {
                "titles": title,
                "links": link,
                "descriptions": desc,
            }
        if self.type == "Marketplace":
            title_tag = single_result.find('a', class_=None)
            title = title_tag.get('title')
            link = title_tag.get('href')
            desc = None
            categories = list()
            desc_tag = single_result.find('text-gray-light')
            if desc_tag:
                desc = desc_tag.text
            categories_tags = single_result.find('a', class_='topic-tag')
            if categories_tags:
                for i in categories_tags:
                    categories.append(str(i).strip('\n '))
            return {
                "titles": title,
                "links": link,
                "descriptions": desc,
                "categories": categories,
            }
        if self.type == "Packages":
            title_tag = single_result.find('a', class_='v-align-middle')
            title = title_tag.text
            ref_link = title_tag.get('href')
            link = self.base_url + ref_link
            desc = single_result.find('p', class_='col-12').text.strip('\n ')
            return {
                "titles": title,
                "links": link,
                "descriptions": desc,
            }
        if self.type == "Issues":
            title_tag = single_result.find('a', class_=None)
            title = title_tag.text
            ref_link = title_tag.get('href')
            link = self.base_url + ref_link
            desc = single_result.find('p', class_=None).text
            span = single_result.find('span', class_='flex-auto')
            opened_by = self.base_url + span.find('a').get('href')
            opened_on = span.find('relative-time').text
            return {
                "titles": title,
                "links": link,
                "descriptions": desc,
                "opened_by": opened_by,
                "opened_on": opened_on,
            }
        if self.type == "Commits":
            title_p = single_result.find('p', class_="commit-title")
            title_tag = title_p.find('a')
            title = title_tag.get('aria-label').strip("\n ")
            ref_link = title_tag.get('href')
            if ref_link.startswith("http"):
                link = ref_link
            else:
                link = self.base_url + ref_link
            opened_on = None
            author = None
            if single_result.find('relative-time'):
                opened_on = single_result.find('relative-time').text
            desc = None
            if single_result.find('a', class_='commit-author'):
                author_tag = single_result.find('a', class_='commit-author')
                author = author_tag.text
                div = single_result.find('div', class_='min-width-0')
                repo = div.find('a', class_=None).text
                desc = "Committed to {}".format(repo)
            return {
                "titles": title,
                "links": link,
                "descriptions": desc,
                "authors": author,
                "opened_on": opened_on,
            }
