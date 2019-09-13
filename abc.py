from search_engine_parser import BaiduSearch
import pprint

search_args = ('preaching to the choir', 3)
bsearch = BaiduSearch()
bresults = bsearch.search(*search_args)
a = {
		"Baidu": bresults
	}
	# pretty print the result from each engine
for k, v in a.items():
	print(f"-------------{k}------------")
	pprint.pprint(v)
	# print 6th description from bing search
print(bresults["descriptions"][0])