import os
import unittest
from importlib import import_module
from urllib.parse import urlparse

import vcr
from parameterized import parameterized_class

from search_engine_parser.core.exceptions import NoResultsOrTrafficError


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
@parameterized_class(('name', 'engine'), get_engines())
class EngineTests(unittest.TestCase):
    """ Testbase for Engines

    provides tests for titles, description and return urls
    """
    engine_class = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        search_args = ('Preaching the choir', 1)
        try:
            with vcr.use_cassette('fixtures/{}-synopsis.yaml'.format(cls.name), record_mode='once'):
                cls.results = cls.engine.search(*search_args)
        except NoResultsOrTrafficError:
            raise unittest.SkipTest(
                '{} failed due to traffic'.format(
                    cls.engine))

    def test_returned_results(self):
        """ 
        Test that the returned results have valid data. 8 is just a chosen value as most search
        engines return values more than that
        """
        self.assertTrue(len(self.results['titles']) >= 8)
        self.assertTrue(len(self.results['links']) >= 8)
        self.assertTrue(len(self.results['descriptions']) >= 8)

    def test_links(self):
        print("{}:::::".format(self.name))
        for link in self.results['links']:
            self.assertTrue(validate_url(link))

    def test_results_length_are_the_same(self):
        """ Tests if returned result items are equal. 
        :param args: a list/tuple of other keys returned
        """
        items = self.results.keys()
        items_set = set(map(lambda x: len(self.results[x]), items))

        self.assertTrue(len(items_set) == 1)
