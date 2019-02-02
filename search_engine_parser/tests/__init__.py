"""
    Test suite using doctest

>>> search_args = ('preaching to the choir', 1)

>>> engine = YahooSearch()
>>> results = engine.search(*search_args)
Got Results
>>> print(len(results['titles']))
10

>>> engine = GoogleSearch()
>>> results = engine.search(*search_args)
Got Results
>>> print(len(results['titles']))
10

>>> engine = BingSearch()
>>> results = engine.search(*search_args)
Got Results
>>> print(len(results['titles']))
10
"""


if __name__=="__main__":
    import doctest
    import sys, os
    sys.path.insert(0, os.getcwd())
    from core import YahooSearch, GoogleSearch, BingSearch
    from core import cli
    doctest.testmod(verbose=True)