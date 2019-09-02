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

ENGINE_SUMMARY = {
    "Google": """
\tNo need for further introductions. The search engine giant holds the first place in search with a stunning difference of 65% from second in place Bing.\n\tAccording to the latest netmarketshare report (November 2018) 73% of searches were powered by Google and only 7.91% by Bing.\n\tGoogle is also dominating the mobile/tablet search engine market share with 81%!
            """,
    "Yahoo": """
\tYahoo is one the most popular email providers and holds the fourth place in search with 3.90% market share.\n\tFrom October 2011 to October 2015, Yahoo search was powered exclusively by Bing. \n\tSince October 2015 Yahoo agreed with Google to provide search-related services and since then the results of Yahoo are powered both by Google and Bing. \n\tYahoo is also the default search engine for Firefox browsers in the United States (since 2014).
            """,
    "Bing": """
\tBing is Microsoft’s attempt to challenge Google in search, but despite their efforts they still did not manage to convince users that their search engine can be an alternative to Google.\n\tTheir search engine market share is constantly below 10%, even though Bing is the default search engine on Windows PCs.
            """,
    "DuckDuckGo": """
\tHas a number of advantages over the other search engines. \n\tIt has a clean interface, it does not track users, it is not fully loaded with ads and has a number of very nice features (only one page of results, you can search directly other web sites etc).\n\tAccording to DuckDuckGo traffic stats [December, 2018], they are currently serving more than 30 million searches per day.
            """,
}