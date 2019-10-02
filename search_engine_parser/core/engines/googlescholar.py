"""@desc
		Parser for google scholar search results
"""

import re
from search_engine_parser.core.base import BaseSearch


class GoogleScholarSearch(BaseSearch):
    """
    Searches Google Scholar for string
    """
    name = "GoogleScholar"
    search_url = "https://scholar.google.gr/scholar?start={page}&q={query}&hl=en"
    summary = "\tGoogle Scholar is a freely accessible web search engine that indexes the full "\
            "text or metadata of scholarly literature across an array of publishing formats and "\
            "disciplines."

    def parse_soup(self, soup):
        """
        Parses Google Scholar Search Soup for results
        """
        # find all class_='gs_r gs_or gs_scl' => each result
        return soup.find_all('div', class_='gs_r gs_or gs_scl')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="gs_r gs_or gs_scl">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link, description, file link, result type of single result
        :rtype: dict
        """
        r_elem = single_result.find('h3', class_='gs_rt')
        link_tag = r_elem.find('a')
        if link_tag:
            raw_link = link_tag.get('href')
        else:
            raw_link = ''

        desc = single_result.find('div', class_='gs_rs')
        if desc:
            desc = desc.text
        else:
            desc = ''

        title = r_elem.text

        t_elem = single_result.find('span', class_='gs_ct1')
        if t_elem:
            result_type = t_elem.text
        else:
            result_type = ''

        f_elem = single_result.find('div', class_='gs_or_ggsm')
        if f_elem:
            flink_tag = r_elem.find('a')
            if flink_tag:
                file_link = flink_tag.get('href')
            else:
                file_link = ''
        else:
            file_link = ''

        title = re.sub(r'^[\[\w+\]]+ ', '', title)

        rdict = {
            "titles": title,
            "links": raw_link,
            "descriptions": desc,
            "result_types": result_type,
            "files_links": file_link
        }
        return rdict
