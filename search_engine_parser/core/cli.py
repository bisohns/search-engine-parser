"""@desc
		Making use of the parser through cli
"""
from __future__ import print_function

import argparse
import sys
from importlib import import_module

from blessed import Terminal
from search_engine_parser import __version__
from search_engine_parser.core.base import ReturnType
from search_engine_parser.core.exceptions import NoResultsOrTrafficError


def display(results, term, **args):
    """ Displays search results
    """
    def print_one(kwargs):
        """ Print one result to the console """
        # Header
        if kwargs.get("titles"):
            print("\t{}".format(term.magenta(kwargs.pop("titles"))))
        if kwargs.get("links"):
            print("\t{}".format(kwargs.pop("links")))
            print("\t-----------------------------------------------------")
        if kwargs.get("descriptions"):
            print(kwargs.pop("descriptions"))
        if kwargs.values():
            for k, v in kwargs.items():
                if v:
                    print(k.strip(), " : ", v)
        print("\n")


    if args.get('rank') and args["rank"] > 10:
        sys.exit(
            "Results are only limited to 10, specify a different page number instead")

    if not args.get('rank'):
        len_results = 0
        for i in results:
            print_one(i)
    else:
        rank = args["rank"]
        print_one(results[rank])
            


def main(args):  # pylint: disable=too-many-branches
    """
        Executes logic from parsed arguments
    """
    term = Terminal()
    engine = args['engine']
    try:
        module = import_module(f"search_engine_parser.core.engines.{engine.lower()}")
        engine_class = getattr(module, "Search")
    except (ImportError, ModuleNotFoundError):
        sys.exit('Engine < {} > does not exist'.format(engine))

    # check if in summary mode
    if args.get("show"):
        print("\t{}".format(term.magenta(engine_class.name)))
        print("\t-----------------------------------------------------")
        print(engine_class.summary)
        sys.exit(0)

    # Initialize search Engine with required params
    engine = engine_class()
    try:
        # Display full details: Header, Link, Description
        results = engine.search(args['query'], args['page'], return_type=ReturnType(args["type"]), url=args.get("url"))
        display(results, term, type=args.get('type'), rank=args.get('rank'))
    except NoResultsOrTrafficError as exc:
        print('\n', '{}'.format(term.red(str(exc))))


def runner():
    """
    runner that handles parsing logic
    """
    parser = argparse.ArgumentParser(description='SearchEngineParser', prog="pysearch")

    parser.add_argument('-V', '--version', action="version", version="%(prog)s v" + __version__)
    parser.add_argument(
        '-e', '--engine',
        help='Engine to use for parsing the query e.g google, yahoo, bing,'
             'duckduckgo (default: google)',
        default='google')
    # add subparsers for summary mode and search mode
    subparsers = parser.add_subparsers(help='help for subcommands')

    parser_search = subparsers.add_parser('search', help='search help')

    parser_search.add_argument(
        '-u',
        '--url',
        help='A custom link to use as base url for search e.g google.de')

    parser_search.add_argument(
        '-q',
        '--query',
        help='Query string to search engine for',
        required=True)
    parser_search.add_argument(
        '-p',
        '--page',
        type=int,
        help='Page of the result to return details for (default: 1)',
        default=1)
    parser_search.add_argument(
        '-t', '--type',
        help='Type of detail to return i.e full, links, desciptions or titles (default: full)',
        default="full")
    parser_search.add_argument(
        '-r',
        '--rank',
        type=int,
        help='ID of Detail to return e.g 5 (default: 0)')

    parser_summary = subparsers.add_parser('summary', help='summary help')
    parser_summary.add_argument(
        '-s',
        '--show',
        type=int,
        help='Show engine description (default: 1)',
        default=1)

    args = vars(parser.parse_args())
    main(args)


if __name__ == '__main__':
    runner()
