"""@desc 
		Parser for Baidu search results
"""

from search_engine_parser.core.base import BaseSearch
import re

class BaiduSearch(BaseSearch):
	"""
	Searches Baidu for string
	"""
	name = "Baidu"
	search_url = "https://www.baidu.com/s?wd={query}&pn={offset}&oq={query}"
	summary = "\tBaidu, Inc. is a Chinese multinational technology company specializing in"\
	" Internet-related services and products and artificial intelligence (AI), headquartered"\
	" in Beijing's Haidian District.\n\tIt is one of the largest AI and internet"\
	" companies in the world.\n\tBaidu offers various services, including a"\
	" Chinese search engine, as well as a mapping service called Baidu Maps."

	
	"""Override get_search_url"""
	def get_search_url(self, query=None, page=None):
		""" 
		Return a formatted search url.
		Offsets are of form 0,10,20, etc. So if 1 is passed, we make it 0, for 2->(2-1)*10=10. etc.
		"""
		
		offset = (page - 1) * 10
		return  self.search_url.format(query=query, page=page, offset=offset)
	
	
	def parse_soup(self, soup):
		"""
		Parses Baidu for a search query
		"""
		
		"""Baidu search can be made deterministic via an id.
		Hence, a regex is used to match all eligible ids
		"""

		return soup.find_all('div',{'id':re.compile(r"^\d{1,2}")})

	def parse_single_result(self, single_result):
		"""
		Parses the source code to return

		:param single_result: single result found in div with a numeric id
		:type single_result: `bs4.element.Tag`
		:return: parsed title, link and description of single result
		:rtype: str, str, str
		"""
		
		h3 = single_result.find('h3')
		link_tag = single_result.find('a')
			
		''' Get the text and link '''
			
		title = single_result.find('h3').text
		link = link_tag.get('href')
			
		desc = single_result.find('div',class_='c-abstract').text
		
		return title, link, desc
