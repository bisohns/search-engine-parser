"""@desc
		Parser for YouTube search results
"""
from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem


class Search(BaseSearch):
    """
    Searches YouTube for string
    """
    name = "YouTube"
    base_url = "https://youtube.com"
    search_url = base_url + "/results?"
    summary = "\tYouTube is an American video-sharing website headquartered in San Bruno, "\
        "California. Three former PayPal employees—Chad Hurley, Steve Chen, and Jawed "\
        "Karim—created the service in February 2005.\n\tGoogle bought the site in November "\
        "2006 for US$1.65 billion; YouTube now operates as one of Google's subsidiaries. "\
        "As of May 2019, more than 500 hours of video content are uploaded to YouTube every minute"

    def get_params(self, query=None, page=None, offset=None, **kwargs):
        params = {}
        params["search_query"] = query
        return params

    def parse_soup(self, soup):
        """
        Parses YouTube for a search query.
        """
        # find all ytd-video-renderer tags
        return soup.find_all('div', class_='yt-lockup-content')

    def parse_single_result(self, single_result, return_type=ReturnType.FULL, **kwargs):
        """
        Parses the source code to return

        :param single_result: single result found in <ytd-video-renderer class="style-scope">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        rdict = SearchItem()
        # pylint: disable=too-many-locals
        title_tag = single_result.find('a', class_='yt-uix-tile-link')
        channel_name = ""

        if return_type in (ReturnType.FULL, return_type.TITLE):
            # Get the text and link
            rdict["titles"] = title_tag.text

        # try for single videos
        try:
            if return_type in (ReturnType.FULL, ReturnType.LINK):
                ref_link = title_tag.get('href')
                link = self.base_url + ref_link
                rdict["links"] = link

            if return_type in (ReturnType.FULL, return_type.DESCRIPTION):
                desc = single_result.find(
                    'div', class_="yt-lockup-description").text
                rdict["descriptions"] = desc

            if return_type in (ReturnType.FULL, ):
                duration = single_result.find(
                    'span', class_='accessible-description').text
                ul_tag = single_result.find('ul', class_='yt-lockup-meta-info')

                channel_name = single_result.find(
                    'a', class_='yt-uix-sessionlink spf-link').text
                views_and_upload_date = ul_tag.find_all('li')
                upload_date = views_and_upload_date[0].text
                views = views_and_upload_date[1].text
                rdict.update({
                    "channels": channel_name,
                    "durations": duration,
                    "views": views,
                    "upload_dates": upload_date,
                })
        except BaseException:  # pylint: disable=broad-except
            link_tags = single_result.find_all(
                'a', class_='yt-uix-sessionlink spf-link')
            # TODO Optimize calls here so that we don't assign ref_link and channel_name
            # when we don't need them
            for i in link_tags:
                if i.get("href").startswith("/playlist"):
                    ref_link = i.get("href")
                elif i.get("href").startswith("/user"):
                    channel_name = i.text
            if return_type in (ReturnType.FULL, ReturnType.LINK):
                link = self.base_url + ref_link
                rdict["links"] = link

            if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
                desc = single_result.find(
                    'span', class_='accessible-description').text
                rdict["descriptions"] = desc
            if return_type in (ReturnType.FULL,):
                rdict.update({
                    "channels": channel_name,
                })
        return rdict
