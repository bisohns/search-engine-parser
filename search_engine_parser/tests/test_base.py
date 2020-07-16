import os
import unittest
from importlib import import_module
from urllib.parse import urlparse
from unittest.mock import patch, MagicMock

import vcr
from parameterized import parameterized_class

from search_engine_parser.core.exceptions import NoResultsOrTrafficError

SEARCH_ARGS = ('Preaching to the choir', 1)


def get_engines():
    """ Returns a list of all engines for tests """
    engines = []

    base_dir = os.getcwd()
    engines_dir = os.path.join(base_dir, 'search_engine_parser', 'core', 'engines')

    for filename in os.listdir(engines_dir):
        if os.path.isfile(os.path.join(engines_dir, filename)) and filename.endswith('.py') \
                and filename != '__init__.py':
            engine = filename.split('.py')[0]
            module = import_module("search_engine_parser.core.engines.{}".format(engine.lower()))
            engine_class = getattr(module, "Search")
            engines.append([engine, engine_class(),])
    return engines


def validate_url(url):
    """ Checks if a url is valid
    urls must contain scheme, netloc and path
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except BaseException:  # pylint: disable=broad-except
        print("URL: %s\n" % url)
        return False


# pylint: disable=no-member
class EngineBaseTest(unittest.TestCase):
    """ Testbase for Engines

    provides tests for engine methods
    """
    @classmethod
    def vcr_search(cls, *args, **kwargs):
        with vcr.use_cassette('fixtures/{}-synopsis.yaml'.format(cls.name), record_mode='new_episodes'):
            cls.results = cls.engine.search(*args, **kwargs)

    def setUp(self):
        from search_engine_parser.core.engines.google import Search # pylint: disable=import-outside-toplevel
        self.engine = Search()

    @patch('search_engine_parser.core.engines.google.Search.get_results')
    @patch('search_engine_parser.core.engines.google.Search.get_soup')
    async def test_urls(self, get_results_mock, get_soup_mock):
        """ Test that url updates work fine """
        await self.engine.search(query="hello", url="google.com.tr")
        first_url = self.engine._parsed_url.geturl()
        self.assertTrue(validate_url(first_url))

        self.engine.search(query="World", url="https://google.com.tr")
        second_url = self.engine._parsed_url.geturl()
        self.assertTrue(validate_url(second_url))

        self.assertNotEqual(second_url, first_url)

    # Test for https://github.com/bisoncorps/search-engine-parser/issues/92
    def test_two_queries_different_results(self):
        """ Test that url updates work fine """
        from search_engine_parser.core.engines.google import Search as GoogleSearch # pylint: disable=import-outside-toplevel
        from search_engine_parser.core.engines.yahoo import Search as YahooSearch # pylint: disable=import-outside-toplevel
        gengine = GoogleSearch()
        yahoo_engine = YahooSearch()
        gresults = gengine.search(query="Hello From the Other Side")
        yresults = yahoo_engine.search(query="this is example Bob")
        for key in gresults[0]:
            self.assertNotEqual(gresults[0].get(key, "GSearch"), yresults[0].get(key, "Ysearch"))

        self.assertNotEqual(gresults, yresults)

# pylint: disable=no-member
@parameterized_class(('name', 'engine'), get_engines())
class TestScraping(unittest.TestCase):
    """ Testbase for Engines

    provides tests for titles, description and return urls
    """
    engine_class = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        try:
            cls.vcr_search(*SEARCH_ARGS)
        except NoResultsOrTrafficError:
            raise unittest.SkipTest(
                '{} failed due to traffic'.format(
                    cls.engine))

    @classmethod
    def vcr_search(cls, *args, **kwargs):
        with vcr.use_cassette('fixtures/{}-synopsis.yaml'.format(cls.name), record_mode='once'):
            cls.results = cls.engine.search(*args, **kwargs)

    @classmethod
    def test_cache_used(cls):
        """
        Test that the cache was used
        """
        try:
            cls.vcr_search(*SEARCH_ARGS)
            if cls.engine._cache_hit == False:
                assert False, "{} cache - unexpected miss".format(
                    cls.engine.name)
        except NoResultsOrTrafficError:
            raise unittest.SkipTest(
                '{} failed due to traffic'.format(
                    cls.engine))

    @classmethod
    def test_cache_not_used(cls):
        """
        Test that the cache was used
        """
        search_args = ('Another random test', 1)
        try:
            cls.vcr_search(*search_args)
            if cls.engine._cache_hit == True:
                assert False, "{} cache - unexpected hit".format(
                    cls.engine.name)
        except NoResultsOrTrafficError:
            raise unittest.SkipTest(
                '{} failed due to traffic'.format(
                    cls.engine))

    @classmethod
    def test_cache_bypassed(cls):
        """
        Test that cache was bypassed
        """
        # wrongly set cls.engine._cache_hit
        cls.engine._cache_hit = True
        search_args = ('Fake cache bypass', 1)
        search_kwargs = {"cache": False}
        try:
            cls.vcr_search(*search_args, **search_kwargs)
            if cls.engine._cache_hit == True:
                assert False, "{} cache - not bypassed".format(
                    cls.engine.name)
        except NoResultsOrTrafficError:
            raise unittest.SkipTest(
                '{} failed due to traffic'.format(
                    cls.engine))

    def test_search_urls(self):
        """
        Test that the search urls generated are valid
        """
        self.assertTrue(validate_url(self.engine._parsed_url.geturl()))

    def test_returned_results(self):
        """
        Test that the returned results have valid data. 8 is just a chosen value as most search
        engines return values more than that
        """
        self.assertTrue(len(self.results['titles']) >= 8)
        self.assertTrue(len(self.results['links']) >= 8)
        # coursera does not return descriptions for 
        # Preaching to the choir
        if not self.engine.name.lower() == "coursera":
            self.assertTrue(len(self.results['descriptions']) >= 8)
        else:
            self.assertTrue(len(self.results["difficulties"]) >= 8)

    def test_links(self):
        print("{}:::::".format(self.name))
        for link in self.results['links']:
            self.assertTrue(validate_url(link))

    def test_results_length_are_the_same(self):
        """ Tests if returned result items are equal.
        :param args: a list/tuple of other keys returned
        """
        # Different engines have different keys which may be returned or not returned
        # So if all keys are not the same length check that the titles and links length are
        # the same
        default_keys = ["titles", "links"]
        default_keys_set = set(map(lambda x: len(self.results[x]), default_keys))

        items = self.results.keys()
        items_set = set(map(lambda x: len(self.results[x]), items))

        self.assertTrue(len(items_set) == 1 or len(default_keys_set) == 1)
