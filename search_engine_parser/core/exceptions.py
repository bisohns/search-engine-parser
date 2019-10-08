"""@desc
    Exceptions
"""


class NoResultsFound(Exception):
    pass


class NoResultsOrTrafficError(Exception):
    """ When No results is returned or unusual traffic caused app to return empty results """

class IncorrectKeyWord(Exception):
    """ When a wrong keyword argument is passed to the search function """
