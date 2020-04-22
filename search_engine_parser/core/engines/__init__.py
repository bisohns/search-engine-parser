from .google import GoogleSearch
from .googlescholar import GoogleScholarSearch
from .yahoo import YahooSearch
from .bing import BingSearch
from .duckduckgo import DuckDuckGoSearch
from .aol import AolSearch
from .yandex import YandexSearch
from .stackoverflow import StackOverflowSearch
from .baidu import BaiduSearch
from .github import GitHubSearch
from .ask import AskSearch
from .youtube import YouTubeSearch
from .myanimelist import MyAnimeListSearch
from .googlenews import GoogleNewsSearch


ENGINE_DICT = {
    'google': GoogleSearch,
    'yahoo': YahooSearch,
    'bing': BingSearch,
    'duckduckgo': DuckDuckGoSearch,
    'yandex': YandexSearch,
    'stackoverflow': StackOverflowSearch,
    'github': GitHubSearch,
    'ask': AskSearch,
    'youtube': YouTubeSearch,
    'baidu': BaiduSearch,
    'aol': AolSearch,
    'myanimelist': MyAnimeListSearch,
    'googlescholar': GoogleScholarSearch,
    'googlenews': GoogleNewsSearch,
}
