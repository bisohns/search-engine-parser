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
        Parse command line arguments
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
    pprint.pprint(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SearchEngineParser')
    parser.add_argument('-e','--engine', help='Engine to use for parsing the query e.g yahoo, defaults to google', default='google')
    parser.add_argument('-q', '--query', help='Query string to search engine for', required=True)
    parser.add_argument('-p', '--page', help='Page of the result to return details for', default=1)

    args = vars(parser.parse_args())
    main(args)
