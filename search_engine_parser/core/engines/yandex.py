"""@desc 
		Parser for Yandex search results
"""

from search_engine_parser.core.base import BaseSearch


class YandexSearch(BaseSearch):
	"""
	Searches Yandex for string
	"""
	name = "Yandex"
	search_url = "https://yandex.com/search/?text={query}&p={offset}"
	summary = "\tYandex is the largest technology company in Russia and the"\
	" largest search engine on the internet in Russian"\
	", with a market share of over 52%."\
	"\n\tThe Yandex.ru home page is the 4th most popular website in Russia."\
	"\n\tIt also has the largest market share of any search engine in the Commonwealth"\
	" of Independent States and is the 5th largest search engine worldwide"\
	" after Google, Baidu, Bing, and Yahoo!"

	def parse_soup(self, soup):
		"""
		Parses Yandex for a search query
		"""
		# find all divs
		return soup.find_all('li',class_="serp-item")

	def parse_single_result(self, single_result):
		"""
		Parses the source code to return

		:param single_result: single result found in <li class="serp-item">
		:type single_result: `bs4.element.ResultSet`
		:return: parsed title, link and description of single result
		:rtype: str, str, str
		"""
		h3 = single_result.find('div',class_="organic__url-text")
		
		link_tag = single_result.find('a')
		
		desc = single_result.find('div',class_="organic__content-wrapper")
		
		''' Get the text and link '''
		title = h3.text
		'''Handle read more type texts'''
		index = title.find("Read more")
		if index >=0:
			title = title[0:int(index)]
		link = link_tag.get('href')
		desc = desc.text
		return title, link, desc

