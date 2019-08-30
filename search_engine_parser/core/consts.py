"""@desc 
		Constants
"""


# Links to search for 10 Query results
SEARCH_QUERY = {
    "Google": 'https://www.google.com/search?q={}&start={}',
    "Yahoo": 'https://search.yahoo.com/search?p={}&b={}',
    "Bing": 'https://www.bing.com/search?q={}&count=10&offset=0&first={}&FORM=PERE',
    # FIXME: Get A Way to return fixed amount of results on DuckDuckGo
    "DuckDuckGo": 'https://www.duckduckgo.com/html/?q={}'
}
