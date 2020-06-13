"""@desc
		Parser for GitHub search results
"""
from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem
from search_engine_parser.core.exceptions import IncorrectKeyWord


class Search(BaseSearch):
    """
    Searches GitHub for string
    """
    name = "GitHub"
    base_url = "https://github.com"
    search_url = base_url + "/search?"
    summary = "\tGitHub is an American company that provides hosting for software development "\
        "version control using Git. It is a subsidiary of Microsoft, which acquired the company "\
        "in 2018 for $7.5 billion.\n\tIt offers all of the distributed version control and source"\
        " code management (SCM) functionality of Git as well as adding its own features."\
        "\n\tAs of May 2019, GitHub reports having over 37 million users and more than 100 million"\
        " repositories (including at least 28 million public repositories), making it the largest "\
        "host of source code in the world."

    def get_params(self, query=None, page=None, offset=None, **kwargs):
        params = {}
        params["q"] = query
        params["p"] = page
        params["type"] = kwargs.get("type_", None)
        self.type = params["type"]
        return params

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
            "RegistryPackages",
            "Issues",
            "Commits",
            "Code")
        if self.type not in allowed_types:
            raise IncorrectKeyWord(
                "No type <{type_}> exists".format(type_=self.type))
        # find all li tags
        if self.type in (None, "Repositories"):
            return soup.find_all('li', class_='repo-list-item')
        elif self.type == "RegistryPackages":
            return soup.find_all("div", class_='hx_hit-package')
        # find all user divs
        elif self.type == "Users":
            return soup.find_all('div', class_='user-list-item')
        elif self.type == "Wikis":
            return soup.find_all('div', class_='hx_hit-wiki')
        elif self.type == "Topics":
            return soup.find_all('div', class_='topic-list-item')
        elif self.type == "Issues":
            return soup.find_all('div', class_='issue-list-item')
        elif self.type == "Marketplace":
            return soup.find_all('div', class_='hx_hit-marketplace')
        elif self.type == "Commits":
            return soup.find_all('div', class_='commits-list-item')

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in container element
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        rdict = SearchItem()
        if self.type in (None, "Repositories"):
            h3 = single_result.find(
                'div', class_='f4')  # pylint: disable=invalid-name
            link_tag = h3.find('a')
            # Get the text and link
            if return_type in (ReturnType.FULL, ReturnType.TITLE):
                title = link_tag.text
                rdict["titles"] = title

            if return_type in (ReturnType.FULL, ReturnType.LINK):
                ref_link = link_tag.get('href')
                link = self.base_url + ref_link
                rdict["links"] = link

            if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
                desc = single_result.find('p', class_="mb-1")
                rdict["descriptions"] = desc.text

            if return_type in (ReturnType.FULL,):
                stars_and_lang_div = single_result.find(
                    'div', class_='d-flex')
                lang = stars_and_lang_div.find(
                    'span', itemprop="programmingLanguage")
                stars = single_result.find('div', class_='mr-3').find(
                    'a')
                updated_on = single_result.find("relative-time").get("title")
                rdict.update({
                    "stars": "" if not stars else stars.text.strip(),
                    "languages": lang.text if lang else "",
                    "updated_on": updated_on,
                })

        if self.type == "Users":
            title_tag = single_result.find('div', class_='f4')
            if return_type in (ReturnType.FULL, ReturnType.TITLE):
                title = title_tag.text
                rdict["titles"] = title

            if return_type in (ReturnType.FULL, ReturnType.LINK):
                ref_link = title_tag.find('a').get('href')
                link = self.base_url + ref_link
                rdict["links"] = link

            if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
                desc_tag = single_result.find('p', class_='mb-1')
                desc = None
                if desc_tag:
                    desc = desc_tag.text.strip(' \n')
                rdict["descriptions"] = desc

            if return_type in (ReturnType.FULL, ):
                location_div = single_result.find('div', class_='d-flex')
                location_and_email = location_div.find_all(
                    'div', class_='mr-3')
                location = email = None
                for single in location_and_email:
                    if single.get('href') == None:
                        location = single.text.strip(' \n')
                    else:
                        email = single.text

                rdict.update({
                    "locations": location,
                    "emails": email,
                })

        if self.type == "Wikis":
            title_tag = single_result.find('a', class_=None)

            if return_type in (ReturnType.FULL, ReturnType.TITLE):
                title = title_tag.get('title')
                rdict["title"] = title

            if return_type in (ReturnType.FULL, ReturnType.LINK):
                ref_link = title_tag.get('href')
                link = self.base_url + ref_link
                rdict["links"] = link

            if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
                desc = single_result.find('p', class_="mb1").text
                rdict["descriptions"] = desc

            if return_type in (ReturnType.FULL, ):
                last_updated = single_result.find(
                    'relative-time').get('title')
                repository = single_result.find('a', class_='muted-link').text
                rdict.update({
                    "repositories": repository,
                    "last_updated": last_updated,
                })

        if self.type == "Topics":
            title_div = single_result.find('div', class_='f4')
            title_tag = title_div.find('a', class_=None)
            if return_type in (ReturnType.FULL, ReturnType.TITLE):
                rdict["titles"] = title_tag.text
            if return_type in (ReturnType.FULL, ReturnType.LINK):
                ref_link = title_tag.get('href')
                link = self.base_url + ref_link
                rdict["links"] = link
            if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
                desc = None
                desc_tag = single_result.find('p', class_=None)
                if desc_tag:
                    desc = desc_tag.text
                rdict["descriptions"] = desc

        if self.type == "Marketplace":
            title_tag = single_result.find('a', class_='no-underline')
            if return_type in (ReturnType.FULL, ReturnType.TITLE):
                title = title_tag.get('title')
                rdict["titles"] = title_tag.text
            if return_type in (ReturnType.FULL, ReturnType.LINK):
                link = title_tag.get('href')
                rdict["links"] = link

            if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
                desc = None
                desc_tag = single_result.find('text-gray')
                if desc_tag:
                    desc = desc_tag.text
                rdict["descriptions"] = desc

            if return_type in (ReturnType.FULL, ):
                categories = list()
                categories_tags = single_result.find_all('a', class_='Label')
                if categories_tags:
                    for i in categories_tags:
                        categories.append(str(i).strip('\n '))
            rdict["categories"] = categories

        if self.type == "RegistryPackages":
            title_tag = single_result.find('a', class_='h4')
            if return_type in (ReturnType.FULL, ReturnType.TITLE):
                title = title_tag.text
                rdict["titles"] = title_tag.text

            if return_type in (ReturnType.FULL, ReturnType.LINK):
                ref_link = title_tag.get('href')
                link = self.base_url + ref_link
                rdict["links"] = link

            if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
                desc = single_result.find(
                    'p', class_='mb-1').text.strip('\n ')
                rdict["descriptions"] = desc

        if self.type == "Issues":
            title_tag = single_result.find('a', class_=None)
            if return_type in (ReturnType.FULL, ReturnType.TITLE):
                title = title_tag.text
                rdict["titles"] = title_tag.text

            if return_type in (ReturnType.FULL, ReturnType.LINK):
                ref_link = title_tag.get('href')
                link = self.base_url + ref_link
                rdict["links"] = link

            if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
                desc = single_result.find('p', class_='mb-0').text
                rdict["descriptions"] = desc

            if return_type in (ReturnType.FULL, ):
                repository = single_result.find(
                    'div', class_='ml-1').find('a', 'text-bold').text
                opened_by = self.base_url + \
                    single_result.find(
                        'div', class_='mr-3').find('a').get('href')
                opened_on = single_result.find('relative-time').get("title")
                rdict.update({
                    "opened_by": opened_by,
                    "opened_on": opened_on,
                    "respositories": repository,
                })

        if self.type == "Commits":
            title_p = single_result.find('div', class_="f4")
            title_tag = title_p.find('a')

            if return_type in (ReturnType.FULL, ReturnType.TITLE):
                title = title_tag.get('aria-label').strip("\n ")
                rdict["titles"] = title_tag.text

            if return_type in (ReturnType.FULL, ReturnType.LINK):
                ref_link = title_tag.get('href')
                if ref_link.startswith("http"):
                    link = ref_link
                else:
                    link = self.base_url + ref_link
                rdict["links"] = link

            if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
                opened_on = None
                author = None
                if single_result.find('relative-time'):
                    opened_on = single_result.find(
                        'relative-time').get("title")
                desc = None
                if single_result.find('a', class_='commit-author'):
                    author_tag = single_result.find(
                        'a', class_='commit-author')
                    author = author_tag.text
                    div = single_result.find('div', class_='d-flex')
                    repo = div.find('a').text
                    desc = "Committed to {}".format(repo)
                rdict["descriptions"] = desc
                if return_type == ReturnType.FULL:
                    rdict.update({
                        "authors": author,
                        "opened_on": opened_on,
                    })
        return rdict
