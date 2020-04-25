"""@desc
	Tests or individual search engines
"""

from search_engine_parser.core.engines.aol import Search as AolSearch
from search_engine_parser.core.engines.ask import Search as AskSearch
from search_engine_parser.core.engines.baidu import Search as BaiduSearch
from search_engine_parser.core.engines.bing import Search as BingSearch
from search_engine_parser.core.engines.duckduckgo import \
    Search as DuckDuckGoSearch
from search_engine_parser.core.engines.github import Search as GithubSearch
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.googlescholar import \
    Search as GoogleScholarSearch
from search_engine_parser.core.engines.stackoverflow import \
    Search as StackOverflowSearch
from search_engine_parser.core.engines.yahoo import Search as YahooSearch
from search_engine_parser.tests.base import EngineTestBase, EngineTests


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


class GoogleNewsEngineTest(EngineTestBase, EngineTests):
    engine_class = GoogleNewsSearch

    def test_returned_results(self):
        self.assertTrue(len(self.results['titles']) >= 10)
        self.assertTrue(len(self.results['links']) >= 10)
        self.assertTrue(len(self.results['descriptions']) >= 10)
        self.assertTrue(len(self.results['image_url']) >= 10)
        self.assertTrue(len(self.results['news_source']) >= 10)
        self.assertTrue(len(self.results['date']) >= 10)


class BingEngineTest(EngineTestBase, EngineTests):
    engine_class = BingSearch

    def test_returned_results(self):
        self.assertTrue(len(self.results['titles']) >= 8)
        self.assertTrue(len(self.results['links']) >= 8)
        self.assertTrue(len(self.results['descriptions']) >= 8)


class AolSearchTest(EngineTestBase, EngineTests):
    engine_class = AolSearch

    def test_returned_results(self):
        self.assertTrue(len(self.results['titles']) >= 9)
        self.assertTrue(len(self.results['links']) >= 9)
        self.assertTrue(len(self.results['descriptions']) >= 9)


class DuckDuckGoSearchTest(EngineTestBase, EngineTests):
    engine_class = DuckDuckGoSearch


class YandexSearchTest(EngineTestBase, EngineTests):
    engine_class = YandexSearch


class StackOverFlowSearchTest(EngineTestBase, EngineTests):
    engine_class = StackOverflowSearch


class BaiduSearchTest(EngineTestBase, EngineTests):
    engine_class = BaiduSearch


class GithubSearchTest(EngineTestBase, EngineTests):
    engine_class = GitHubSearch


class YoutubeSearchTest(EngineTestBase, EngineTests):
    engine_class = YouTubeSearch


class MyAnimeListSearchTest(EngineTestBase, EngineTests):
    engine_class = MyAnimeListSearch


class AskEngineSearchTest(EngineTestBase, EngineTests):
    engine_class = AskSearch
