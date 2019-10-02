"""@desc
	Tests or individual search engines
"""

from search_engine_parser.core import (
    YahooSearch,
    GoogleSearch,
    GoogleScholarSearch,
    BingSearch,
    DuckDuckGoSearch,
    AolSearch,
    YandexSearch,
    StackOverflowSearch,
    BaiduSearch,
    GitHubSearch,
    YouTubeSearch,
    MyAnimeListSearch,
    AskSearch)
from .base import EngineTestBase, EngineTests


class YahooEngineTest(EngineTestBase, EngineTests):
    engine_class = YahooSearch


class GoogleEngineTest(EngineTestBase, EngineTests):
    engine_class = GoogleSearch

    def test_returned_results(self):
        self.assertTrue(len(self.results['titles']) >= 9)
        self.assertTrue(len(self.results['links']) >= 9)
        self.assertTrue(len(self.results['descriptions']) >= 9)

class GoogleScholarEngineTest(EngineTestBase, EngineTests):
    engine_class = GoogleScholarSearch

    def test_returned_results(self):
        self.assertTrue(len(self.results['titles']) >= 10)
        self.assertTrue(len(self.results['links']) >= 10)
        self.assertTrue(len(self.results['descriptions']) >= 10)
        self.assertTrue(len(self.results['result_types']) >= 10)
        self.assertTrue(len(self.results['files_links']) >= 10)


class BingEngineTest(EngineTestBase, EngineTests):
    engine_class = BingSearch


class AolSearchTest(EngineTestBase, EngineTests):
    engine_class = AolSearch

    def test_returned_results(self):
        self.assertTrue(len(self.results['titles']) >= 9)
        self.assertTrue(len(self.results['links']) >= 9)
        self.assertTrue(len(self.results['descriptions']) >= 9)

class DuckDuckGoSearchTest(EngineTestBase, EngineTests):
    engine_class = DuckDuckGoSearch

    def test_returned_results(self):
        self.assertTrue(len(self.results['titles']) >= 10)
        self.assertTrue(len(self.results['links']) >= 10)
        self.assertTrue(len(self.results['descriptions']) >= 10)


class YandexSearchTest(EngineTestBase, EngineTests):
    engine_class = YandexSearch


class StackOverFlowSearchTest(EngineTestBase, EngineTests):
    engine_class = StackOverflowSearch

    def test_returned_results(self):
        self.assertTrue(len(self.results['titles']) >= 15)
        self.assertTrue(len(self.results['links']) >= 15)
        self.assertTrue(len(self.results['descriptions']) >= 15)


class BaiduSearchTest(EngineTestBase, EngineTests):
    engine_class = BaiduSearch

    def test_returned_results(self):
        self.assertTrue(len(self.results['titles']) >= 8)
        self.assertTrue(len(self.results['links']) >= 8)
        self.assertTrue(len(self.results['descriptions']) >= 8)


class GithubSearchTest(EngineTestBase, EngineTests):
    engine_class = GitHubSearch


class YoutubeSearchTest(EngineTestBase, EngineTests):
    engine_class = YouTubeSearch

    def test_returned_results(self):
        self.assertTrue(len(self.results['titles']) >= 10)
        self.assertTrue(len(self.results['links']) >= 10)
        self.assertTrue(len(self.results['descriptions']) >= 10)


class MyAnimeListSearchTest(EngineTestBase, EngineTests):
    engine_class = MyAnimeListSearch


class AskEngineSearchTest(EngineTestBase, EngineTests):
    engine_class = AskSearch

    def test_returned_results(self):
        self.assertTrue(len(self.results['titles']) >= 8)
        self.assertTrue(len(self.results['links']) >= 8)
        self.assertTrue(len(self.results['descriptions']) >= 8)
