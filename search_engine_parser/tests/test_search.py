"""@desc
    Tests or individual search engines
"""

from search_engine_parser.core import (
    YahooSearch, GoogleSearch, BingSearch, DuckDuckGoSearch, AolSearch
)

search_args = ('preaching to the choir', 1)


def test_yahoo_search():
    engine = YahooSearch()
    results = engine.search(*search_args)
    assert len(results['titles']) == 10


def test_google_search():
    engine = GoogleSearch()
    results = engine.search(*search_args)
    assert len(results['titles']) == 10


def test_bing_search():
    engine = BingSearch()
    # change search args because bing first page always includes video
    bing_search_args = ('preaching to the choir', 2)
    results = engine.search(*bing_search_args)
    assert len(results['titles']) == 10


def test_aol_search():
    engine = AolSearch()
    # change search args because aol first page always includes video
    aol_search_args = ('preaching to the choir', 2)
    results = engine.search(*aol_search_args)
    assert len(results['titles']) == 10


def test_duckduckgo_search():
    engine = DuckDuckGoSearch()
    results = engine.search(*search_args)
    assert len(results['titles']) >= 10
