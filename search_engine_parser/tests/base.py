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
        self.assertTrue(len(self.results['titles']) >= 8)
        self.assertTrue(len(self.results['links']) >= 8)
        self.assertTrue(len(self.results['descriptions']) >= 8)

    def test_links(self):
        for link in self.results['links']:
            self.assertTrue(validate_url(link))

    def test_results_length_are_the_same(self):
        """ Tests if returned result items are equal. 
        :param args: a list/tuple of other keys returned

        This should be overwritten for Engine that return more items
        """
        items = self.results.keys()
        items_set = set(map(lambda x: len(self.results[x]), items))

        self.assertTrue(len(items_set) == 1)
