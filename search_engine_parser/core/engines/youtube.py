"""@desc 
		Parser for YouTube search results
"""
from search_engine_parser.core.base import BaseSearch

class YouTubeSearch(BaseSearch):
    """
    Searches YouTube for string
    """
    name = "YouTube"
    base_url = "https://youtube.com"
    search_url = base_url + "/results?search_query={query}"
    summary = "\tYouTube is an American video-sharing website headquartered in San Bruno, California." \
        "Three former PayPal employees—Chad Hurley, Steve Chen, and Jawed Karim—created the service in February 2005." \
        "\n\tGoogle bought the site in November 2006 for US$1.65 billion; YouTube now operates as one of Google's subsidiaries. "\
        "As of May 2019, more than 500 hours of video content are uploaded to YouTube every minute"
    def parse_soup(self, soup):
        """
        Parses YouTube for a search query.
        """
        # find all ytd-video-renderer tags
        return soup.find_all('div', class_='yt-lockup-content')

    def parse_single_result(self, single_result):
        """
        Parses the source code to return

        :param single_result: single result found in <ytd-video-renderer class="style-scope">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: str, str, str
        """
        title_tag = single_result.find('a', class_='yt-uix-tile-link')
        ''' Get the text and link '''
        title = title_tag.text
        duration = single_result.find('span', class_='accessible-description').text
        ul = single_result.find('ul', class_='yt-lockup-meta-info')

        ref_link = title_tag.get('href')
        link = self.base_url + ref_link

        desc_text = single_result.find('div', class_="yt-lockup-description").text
        channel_name = single_result.find('a', class_='yt-uix-sessionlink spf-link').text
        views_and_upload_date = ul.find_all('li')
        upload_date = views_and_upload_date[0].text
        views = views_and_upload_date[1].text

        try:
            desc = "{} \tUploaded-{} \t{} \n{}".format(views, upload_date, duration, desc_text)
        except:
            desc = "[Playlist] \n{}".format(desc_text)
        title = "{} \n\tChannel - {}".format(title, channel_name)
        return title, link, desc
