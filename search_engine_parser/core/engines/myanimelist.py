"""@desc 
		Parser for MyAnimeList search results
"""

from search_engine_parser.core.base import BaseSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError
import math
import sys
import re

class MyAnimeListSearch(BaseSearch):
	"""
	Searches MyAnimeList for string
	"""
	name = "MyAnimeList"

	search_url = "https://myanimelist.net/anime/genre/{index}/{query}?page={offset}"
	summary = "\tMyAnimeList, often abbreviated as MAL, is an anime and manga social"\
				"networking and social cataloging application website."\
				"\n\tThe site provides its users with a list-like system to organize"\
				"and score anime and manga.\n\tIt facilitates finding users who share"\
				"similar tastes and provides a large database on anime and manga.\n\tThe"\
				"site claims to have 4.4 million anime and 775,000 manga entries."\
				"\n\tIn 2015, the site received over 120 million visitors a month."

	
	"""Override get_search_url"""
	def get_search_url(self, query=None, page=None):
		""" 
		Return a formatted search url.
		In MAL, results 1 to 100 are in page 1, 101-200 in page 2, etc, so modify URL accordingly.
		Also, the genre map helps in transformations such as action->1, adventure->2, and so on.
		"""
		
		genre_map = ["action","adventure","cars","comedy","dementia",
				"demons","drama","ecchi","fantasy","game",
				"harem","hentai","historical","horror","josei",
				"kids","magic","martial arts","mecha","military",
				"music","mystery","parody","police","psychological",
				"romance","samurai","school","sci-fi","seinen",
				"shoujo","shoujo ai","shounen","shounen ai","slice of life",
				"space","sports","super power","supernatural","thriller",
				"vampire","yaoi","yuri"]
		
		offset = math.ceil(page/10)
		query = query.lower()
		self.page = page
		try:
			index = genre_map.index(query) + 1 #Genres start from 1 in MAL
		except ValueError:
			index = -1
		if index == -1:
			raise NoResultsOrTrafficError(
				"The result parsing was unsuccessful. It is either your query could not be found"+
				" or it was flagged as unusual traffic")
		return self.search_url.format(query=query, page=page, index=index, offset=offset)
	
	
	def parse_soup(self, soup):
		"""
		Parses MyAnimeList for a search query
		"""
		
		"""MyAnimeList search can be made deterministic via an id.
		Hence, a regex is used to match all eligible ids
		"""

		return soup.find_all('div', class_="seasonal-anime js-seasonal-anime")

	def parse_single_result(self, single_result):
		"""
		Parses the source code to return

		:param single_result: single result found in div with a numeric id
		:type single_result: `bs4.element.Tag`
		:return: parsed title, link and description of single result
		:rtype: str, str, str
		"""
		
		h3 = single_result.find('p',class_="title-text")
		link_tag = single_result.find('a')
			
		''' Get the text and link '''
			
		title = h3.text
		title = re.sub("\n+","",title)
		link = link_tag.get('href')
			
		desc = single_result.find('div',class_='synopsis').text
		desc = re.sub("\r+","",desc)
		desc = re.sub("\n+","",desc)
		
		return title, link, desc
		
	"""Override this as we want to return only ten results"""
	def parse_result(self, results):
		"""
		Runs every entry on the page through parse_single_result

		:param results: Result of main search to extract individual results
		:type results: list[`bs4.element.ResultSet`]
		:returns: dictionary. Containing titles, links and descriptions.
		:rtype: dict
		"""
		titles = []
		links = []
		descs = []
		
		index = 0
		
		for each in results:
			title = link = desc = " "
			index += 1
			"""Skip all unimportant divs"""
			if index < ((self.page - 1) * 10 + 1) or index > (self.page) * 10:
				continue
			try:
				title, link, desc = self.parse_single_result(each)
				# Append links and text to a list
				titles.append(title)
				links.append(link)
				descs.append(desc)
			except Exception as e:
				print(e)
		search_results = {'titles': titles,
						'links': links,
						'descriptions': descs}
		return search_results