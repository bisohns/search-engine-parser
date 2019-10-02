import unittest
from urllib.parse import urlparse
from search_engine_parser.core.exceptions import NoResultsOrTrafficError


def validate_url(url):
    """ Checks if a url is valid
    urls must contain scheme, netloc and path
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except BaseException: # pylint: disable=broad-except
        return False


class EngineTestBase(unittest.TestCase):
    """ Testbase for Engines

    provides tests for titles, description and return urls
    """
    engine_class = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.engine_class:
            raise Exception("engine_class not defined")

        search_args = ('preaching to the choir', 2)
        cls.engine = cls.engine_class()  # pylint: disable=not-callable
        try:
            cls.results = cls.engine.search(*search_args)
        except NoResultsOrTrafficError:
            raise unittest.SkipTest(
                '{} failed due to traffic'.format(
                    cls.engine))


# pylint: disable=no-member
class EngineTests:

    def test_returned_results(self):
        self.assertEqual(len(self.results['titles']), 10)
        self.assertEqual(len(self.results['links']), 10)
        self.assertEqual(len(self.results['descriptions']), 10)

    def test_links(self):
        for link in self.results['links']:
            self.assertTrue(validate_url(link))
