"""@desc 
		Making use of the parser through cli

 	@author 
 		Domnan Diretnan
 		Artificial Intelligence Enthusiast & Software Engineer.
 		Email: diretnandomnan@gmail.com
 		Github: https://github.com/deven96
 		GitLab: https://gitlab.com/Deven96

 	@project
 		@create date 2019-02-01 22:25:58
 		@modify date 2019-02-01 22:25:58

	@license
		MIT License
		Copyright (c) 2018. Domnan Diretnan. All rights reserved

 """


import argparse
import sys
import pprint
from engines import YahooSearch, GoogleSearch, BingSearch


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
    else:
        sys.exit(f'Engine <args["engine"]> does not exist')
    results = engine.search(args['query'], args['page'])
    if args["type"] and (0 <= args["rank"] < 10):
        type_ = args["type"]
        rank = args["rank"]
        try:
            print(results[type_][rank])
        except Exception as e:
            print(e)

def runner():
    """
    runner that handles parsing logic
    """
    parser = argparse.ArgumentParser(description='SearchEngineParser')
    parser.add_argument('-e','--engine', help='Engine to use for parsing the query e.g yahoo (default: google)', default='google')
    parser.add_argument('-q', '--query', help='Query string to search engine for', required=True)
    parser.add_argument('-p', '--page', type=int, help='Page of the result to return details for (default: 1)', default=1)
    parser.add_argument('-t', '--type', help='Type of detail to return i.e links, desciptions or titles', default="links")
    parser.add_argument('-r', '--rank', type=int, help='Rank of detail in list to return e.g 5 (default: 0)', default=0)

    args = vars(parser.parse_args())
    main(args)

if __name__ == '__main__':
    runner()
