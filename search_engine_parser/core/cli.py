"""@desc 
		Making use of the parser through cli
 """

from __future__ import print_function
import argparse
import sys
from blessed import Terminal

from search_engine_parser.core.engines import *
from search_engine_parser.core.exceptions import NoResultsOrTrafficError


def display(results, term, **args):
    """ Displays search results 
    """

    def print_one(title, link, desc):
        """ Print one result to the console """
        # Header
        print(f"\t{term.magenta(title)}")
        print(f"\t{link}")
        print("\t-----------------------------------------------------")
        print(desc, '\n\n')

    if args.get('rank') and args["rank"] > 10:
        sys.exit("Results are only limited to 10, specify a different page number instead")

    # Display full details: Header, Link, Description
    if args["type"] == "full":
        if not args.get('rank'):
            for title, link, desc in zip(results['titles'], results['links'], results['descriptions']):
                print_one(title, link, desc)
        else:
            rank = args["rank"]
            print_one(results['titles'][rank], results['links'][rank], results['descriptions'][rank])

    else:
        type_ = args["type"]
        if not args.get('rank'):
            for i, result in enumerate(results[type_]):
                print(i, '-->', result, '\n')
        else:
            rank = args["rank"]
            print(results[type_][rank])



def main(args):
    """
        Executes logic from parsed arguments
    """
    term = Terminal()
    engine = args['engine']
    if engine == 'google':
        engine_class = GoogleSearch
    elif engine == 'yahoo':
        engine_class = YahooSearch
    elif engine == 'bing':
        engine_class = BingSearch
    elif engine == 'duckduckgo':
        engine_class = DuckDuckGoSearch
    elif engine == 'yandex':
        engine_class = YandexSearch
    elif engine == 'stackoverflow':
        engine_class = StackOverflowSearch
    elif engine == 'github':
        engine_class = GitHubSearch
    else:
        sys.exit(f'Engine < {engine} > does not exist')
    
    # check if in summary mode
    if args.get("show"):
        print(f"\t{term.magenta(engine_class.name)}")
        print("\t-----------------------------------------------------")
        print(engine_class.summary)
        sys.exit(0)

    # Initialize search Engine with required params
    engine = engine_class()
    try:
        results = engine.search(args['query'], args['page'])
        display(results, term, type=args.get('type'), rank=args.get('rank'))
    except NoResultsOrTrafficError as e:
        print('\n', f'{term.red(str(e))}')



def runner():
    """
    runner that handles parsing logic
    """
    parser = argparse.ArgumentParser(description='SearchEngineParser')
    parser.add_argument('-e','--engine', help='Engine to use for parsing the query e.g google, yahoo, bing, duckduckgo (default: google)', default='google')
    # add subparsers for summary mode and search mode
    subparsers = parser.add_subparsers(help='help for subcommands')

    parser_search = subparsers.add_parser('search', help='search help')

    parser_search.add_argument('-q', '--query', help='Query string to search engine for', required=True)
    parser_search.add_argument('-p', '--page', type=int, help='Page of the result to return details for (default: 1)', default=1)
    parser_search.add_argument('-t', '--type', help='Type of detail to return i.e full, links, desciptions or titles (default: full)', default="full")
    parser_search.add_argument('-r', '--rank', type=int, help='ID of Detail to return e.g 5 (default: 0)')

    parser_summary = subparsers.add_parser('summary', help='summary help')
    parser_summary.add_argument('-s', '--show', type=int, help='Show engine description (default: 1)', default=1)


    args = vars(parser.parse_args())
    main(args)

if __name__ == '__main__':
    runner()
