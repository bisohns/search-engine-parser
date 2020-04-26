"""@desc
		Parser for google search results
"""

from search_engine_parser.core.base import BaseSearch, ReturnType, SearchItem, SearchResult


class Search(BaseSearch):
    """
    Searches Google for string
    """
    name = "Google"
    search_url = "https://www.google.com/search?"
    summary = "\tNo need for further introductions. The search engine giant holds the first "\
        "place in search with a stunning difference of 65% from second in place Bing.\n"\
        "\tAccording to the latest netmarketshare report (November 2018) 73% of searches "\
        "were powered by Google and only 7.91% by Bing.\n\tGoogle is also dominating the "\
        "mobile/tablet search engine market share with 81%!"

    def get_params(self, query=None, offset=None, page=None, **kwargs):
        params = {}
        params["num"] = 10
        params["start"] = page
        params["q"] = query
        params["client"] = "ubuntu"
        return params

    def parse_soup(self, soup):
        """
        Parses Google Search Soup for results
        """
        # find all class_='g' => each result
        return soup.find_all('div', class_='g')

    def parse_result(self, results, **kwargs):
        """
        Runs every entry on the page through parse_single_result

        :param results: Result of main search to extract individual results
        :type results: list[`bs4.element.ResultSet`]
        :returns: dictionary. Containing lists of titles, links, descriptions, direct results and other possible\
            returns.
        :rtype: dict
        """
        search_results = SearchResult()
        for each in results:
            try:
                rdict = self.parse_single_result(each, **kwargs)
                search_results.append(rdict)
            except Exception as e:  # pylint: disable=invalid-name, broad-except
                print("Exception: %s" % str(e))

        direct_answer = self.parse_direct_answer(results[0])
        rdict = {'direct_answer': direct_answer}
        if direct_answer is not None:
            search_results.append(rdict)
        return search_results

    def parse_direct_answer(self, single_result, return_type=ReturnType.FULL):
        # returns empty string when there is no direct answer
        if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
            direct_answer = ''
            if not single_result.find('span', class_='st'):
                # example query: President of US
                if single_result.find('div', class_='Z0LcW'):
                    direct_answer = single_result.find('div', class_='Z0LcW').find('a').text
                
                # example query: 5+5
                elif single_result.find('span', class_='qv3Wpe'):
                    direct_answer = single_result.find('span', class_='qv3Wpe').text            
                
                # example query: Weather in dallas
                elif single_result.find('div', id='wob_wc'):
                    weather_status = single_result.find('span', id='wob_dc').text
                    temperature = single_result.find('span', id='wob_tm').text
                    unit = single_result.find('div', class_='wob-unit').find('span', class_='wob_t').text
                    direct_answer = weather_status + ', ' + temperature + unit  
                
                # example query: 100 euros in pounds
                elif single_result.find('span', class_='DFlfde SwHCTb'):
                    direct_answer = single_result.find('span', class_='DFlfde SwHCTb').text + ' ' +single_result.find('span', class_='MWvIVe').text

                # example query: US time
                elif single_result.find('div', class_="gsrt vk_bk dDoNo"):
                    direct_answer = single_result.find('div', class_='gsrt vk_bk dDoNo').text

                # Christmas
                elif single_result.find('div', class_="zCubwf"):
                    direct_answer = single_result.find('div', class_="zCubwf").text

            
            elif not single_result.find('span', class_='st').text:
                # example queris: How long shoud a car service take?, fastest animal
                if single_result.find('div', class_='Z0LcW'):
                    direct_answer = single_result.find('div', class_='Z0LcW').text
        
        return direct_answer

    def parse_single_result(self, single_result, return_type=ReturnType.FULL):
        """
        Parses the source code to return

        :param single_result: single result found in <div class="g">
        :type single_result: `bs4.element.ResultSet`
        :return: parsed title, link and description of single result
        :rtype: dict
        """
        results = SearchItem()
        r_elem = single_result.find('div', class_='r')

        # Get the text and link
        if return_type in (ReturnType.FULL, return_type.TITLE):
            if r_elem:
                h3_tag = r_elem.find('h3')
                title = h3_tag.text
                if not title:
                    title = h3_tag.find('div', class_='ellip').text
                results['titles'] = title

        if return_type in (ReturnType.FULL, ReturnType.LINK):
            if r_elem:
                link_tag = r_elem.find('a')
                raw_link = link_tag.get('href')
                results['links'] = raw_link

        if return_type in (ReturnType.FULL, ReturnType.DESCRIPTION):
            desc = single_result.find('span', class_='st')
            if desc:
                desc = desc.text
                # quick answer description
                if not desc:
                    desc = single_result.find('span', class_='e24Kjd').text
                results['descriptions'] = desc

        return results
