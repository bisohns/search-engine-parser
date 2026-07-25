import logging
import unittest
from unittest.mock import patch, MagicMock, PropertyMock

from search_engine_parser.core.utils import get_rand_user_agent, USER_AGENT_LIST

FAKE_USERAGENT_LOGGER = logging.getLogger('fake_useragent')


class ListHandler(logging.Handler):
    """ Collects emitted log records for later assertions """

    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


def raise_index_error(*args, **kwargs):
    # Mirrors fake-useragent's own internal behaviour when its cache
    # server is unreachable or returns unexpected data: it logs a
    # WARNING with a full traceback attached (exc_info) before falling
    # back, see fake_useragent/utils.py:load() in the fake-useragent
    # package itself.
    FAKE_USERAGENT_LOGGER.warning(
        'Error occurred during loading data. '
        'Trying to use cache server %s',
        'https://fake-useragent.herokuapp.com',
        exc_info=IndexError('list index out of range'),
    )
    raise IndexError('list index out of range')


class UtilsTest(unittest.TestCase):

    @patch('search_engine_parser.core.utils.UserAgent')
    def test_get_rand_user_agent_falls_back_and_suppresses_warning(self, mock_user_agent_class):
        """
        get_rand_user_agent() must fall back to USER_AGENT_LIST when
        fake_useragent fails internally (bisohns/search-engine-parser#159),
        and the fake_useragent logger must not surface a WARNING-or-above
        record while it does so.
        """
        mock_instance = MagicMock()
        type(mock_instance).random = PropertyMock(side_effect=raise_index_error)
        mock_user_agent_class.return_value = mock_instance

        handler = ListHandler()
        FAKE_USERAGENT_LOGGER.addHandler(handler)
        try:
            result = get_rand_user_agent()
        finally:
            FAKE_USERAGENT_LOGGER.removeHandler(handler)

        warning_or_above = [r for r in handler.records if r.levelno >= logging.WARNING]
        self.assertEqual(
            warning_or_above, [],
            "fake_useragent logger emitted a WARNING-or-above record; "
            "utils.py's suppression should prevent this (see #159)"
        )
        self.assertIn(result, USER_AGENT_LIST)
