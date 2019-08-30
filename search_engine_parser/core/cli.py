"""@desc 
		Making use of the parser through cli
 """


import argparse
import sys
from blessed import Terminal

from search_engine_parser.core.engines import YahooSearch, GoogleSearch, BingSearch, DuckDuckGoSearch

def display(results, **args):
    """ Displays search results 
    """
    term = Terminal()

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
    if args['engine'] == 'google':
        engine = GoogleSearch()
    elif args['engine'] == 'yahoo':
        engine = YahooSearch()
    elif args['engine'] == 'bing':
        engine = BingSearch()
    elif args['engine'] == 'duckduckgo':
        engine = DuckDuckGoSearch()
    else:
        sys.exit(f'Engine <args["engine"]> does not exist')
    results = engine.search(args['query'], args['page'])
    display(results, type=args.get('type'), rank=args.get('rank'))


def runner():
    """
    runner that handles parsing logic
    """
    parser = argparse.ArgumentParser(description='SearchEngineParser')
    parser.add_argument('-e','--engine', help='Engine to use for parsing the query e.g google, yahoo, bing, duckduckgo (default: google)', default='google')
    parser.add_argument('-q', '--query', help='Query string to search engine for', required=True)
    parser.add_argument('-p', '--page', type=int, help='Page of the result to return details for (default: 1)', default=1)
    parser.add_argument('-t', '--type', help='Type of detail to return i.e full, links, desciptions or titles (default: full)', default="full")
    parser.add_argument('-r', '--rank', type=int, help='ID of Detail to return e.g 5')

    args = vars(parser.parse_args())
    main(args)

if __name__ == '__main__':
    runner()
