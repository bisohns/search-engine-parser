"""@desc
	Tests or individual search engines
"""

from search_engine_parser.core import (
	YahooSearch, GoogleSearch, BingSearch, DuckDuckGoSearch, AolSearch, YandexSearch,
	StackOverflowSearch
)
search_args = ('preaching to the choir', 2)


def test_yahoo_search():
	engine = YahooSearch()
	results = engine.search(*search_args)
	assert len(results['titles']) == 10


def test_google_search():
	engine = GoogleSearch()
	results = engine.search(*search_args)
	assert len(results['titles']) >= 9

def test_bing_search():
	engine = BingSearch()
	results = engine.search(*search_args)
	assert len(results['titles']) == 10


def test_aol_search():
	engine = AolSearch()
	results = engine.search(*search_args)
	assert len(results['titles']) == 10


def test_duckduckgo_search():
	engine = DuckDuckGoSearch()
	results = engine.search(*search_args)
	assert len(results['titles']) >= 10

def test_yandex_search():
	engine = YandexSearch()
	results = engine.search(*search_args)
	assert len(results['titles']) >= 9

def test_stackoverflow_search():
	engine = StackOverflowSearch()
	results = engine.search(*search_args)
	assert len(results['titles']) >= 15