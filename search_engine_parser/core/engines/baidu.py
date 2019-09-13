"""@desc 
		Parser for Baidu search results
"""

from search_engine_parser.core.base import BaseSearch

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

	def parse_soup(self, soup):
		"""
		Parses Baidu for a search query
		"""
		
		"""Baidu search can be made deterministic via an id, so add it in self"""
		
		soups=[]
		for i in range(int(self.offset)*10+1,int(self.offset)*10+11):
			soups.append(soup.find('div',id=i))

		return soups

	def parse_single_result(self, single_result):
		"""
		Parses the source code to return

		:param single_result: single result found in <li class="serp-item">
		:type single_result: `bs4.element.ResultSet`
		:return: parsed title, link and description of single result
		:rtype: str, str, str
		"""
		
		h3 = single_result.find('h3')
		link_tag = single_result.find('a')
		
		''' Get the text and link '''
		
		title=h3.text
		link=link_tag.get('href')
		
		desc = single_result.find('div',class_='c-abstract').text

		
		return title, link, desc

