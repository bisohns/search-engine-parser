"""@desc 
		Parser for MyAnimeList search results
"""

from search_engine_parser.core.base import BaseSearch
import math
import re

class MyAnimeListSearch(BaseSearch):
	"""
	Searches MyAnimeList for string
	"""
	name = "MyAnimeList"

	search_url = "https://myanimelist.net/anime.php?q={query}&show={offset}"
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
		In MAL, results 1 to 50 are in page 1, 51-100 in page 2, etc, so modify URL accordingly.
		"""
		
		offset = (math.ceil(page/5) - 1) * 50
		
		self.page = (page - 1) % 5 #Save this value so that we can return 10 results
		return self.search_url.format(query=query, offset=offset)
	
	
	def parse_soup(self, soup):
		"""
		Parses MyAnimeList for a search query
		"""
		
		#The data is stored in table so find all table rows
		return soup.find('div',class_='js-categories-seasonal js-block-list list').find_all('tr')

	
	def parse_single_result(self, single_result):
		"""
		Parses the source code to return

		:param single_result: single result found in div with a numeric id
		:type single_result: `bs4.element.Tag`
		:return: parsed title, link and description of single result
		:rtype: str, str, str
		"""
		
		data = list(single_result.find_all('td'))
		
		title = data[1].find('strong').text.strip()
		
		link_tag = data[1].find('a')
		link = link_tag.get('href')
		
		desc = data[1].find('div',class_='pt4').text.strip()
		desc=desc[0:len(desc)-13] #...Read More is always in desc
		
		animetype = data[2].text.strip()
		
		episodes = data[3].text.strip()
		
		score = data[4].text.strip()
		
		rdict = {
			"titles": title,
			"links": link,
			"descriptions": desc,
			"episode_count": episodes,
			"animetypes": animetype,
			"ratings": score
		}
		return rdict
		
	"""Override this as we want to return only ten results"""
	def parse_result(self, results):
		"""
		Runs every entry on the page through parse_single_result
		:param results: Result of main search to extract individual results
		:type results: list[`bs4.element.ResultSet`]
		:returns: dictionary. Containing titles, links, episodes, scores, types and descriptions.
		:rtype: dict
		"""
		search_results = dict()
		index = -1
		for each in results:
			index +=1
			#Skip the top row of table (always) and unimportant trs (Out of range)
			if index <= 0 or index < self.page * 10 + 1 or index > self.page * 10 + 10:
				continue
			try:
				rdict = self.parse_single_result(each)
				# Create a list for all keys in rdict if not exist, else
				for key in rdict.keys():
					if key not in search_results.keys():
						search_results[key] = list([rdict[key]])
					else:
						search_results[key].append(rdict[key])
			except Exception as e:
				pass
		return search_results