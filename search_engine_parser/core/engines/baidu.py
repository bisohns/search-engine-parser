"""@desc 
		Parser for Baidu search results
"""

from search_engine_parser.core.base import BaseSearch

class BaiduSearch(BaseSearch):
	"""
	Searches Baidu for string
	"""
	offset=None
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
		Adding offset value to self as we would need it in parse_soup
		"""
		
		self.offset = (page - 1) * 10
		return  self.search_url.format(query=query, page=page, offset=self.offset)
	
	
	def parse_soup(self, soup):
		"""
		Parses Baidu for a search query
		"""
		
		"""Baidu search can be made deterministic via an id.
		The id of divs are in range 1-10 for page 1, 11-20 in page 2, so that arithmetic is
		handled by the previous calculation of offset (it transforms 1 to 0, 2 to 10, etc.)
		and we loop for all div's from (10+1==11) to (10+11-1)=20 {-1 due to nature of range function}
		"""
		
		soups=[]
		for i in range(int(self.offset) + 1,int(self.offset) + 11):
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

