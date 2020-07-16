import os
import random
import pickle
import hashlib
import aiohttp

FILEPATH = os.path.dirname(os.path.abspath(__file__))

# prevent caching
USER_AGENT_LIST = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) "
    "Chrome/19.0.1084.46 Safari/536.5",
    "Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) "
    "Chrome/19.0.1084.46 Safari/536.5",
]


def get_rand_user_agent():
    return random.choice(USER_AGENT_LIST)


class CacheHandler:
    def __init__(self):
        if not os.path.exists(os.path.join(FILEPATH, "cache")):
            os.makedirs("cache")
        self.cache = os.path.join(FILEPATH, "cache")
        enginelist = os.listdir(os.path.join(FILEPATH, "engines"))
        self.engine_cache = {i[:-3]: os.path.join(self.cache, i[:-3]) for i in enginelist if i not in
                             ("__init__.py")}
        for cache in self.engine_cache.values():
            if not os.path.exists(cache):
                os.makedirs(cache)

    async def get_source(self, engine, url, headers, cache=True):
        """
        Retrieves source code of webpage from internet or from cache

        :rtype: str, bool
        :param engine: engine of the engine saving
        :param url: URL to pull source code from
        :param headers: request headers to make use of
        :param cache: use cache or not
        """
        encodedUrl = url.encode("utf-8")
        urlhash = hashlib.sha256(encodedUrl).hexdigest()
        engine = engine.lower()
        cache_path = os.path.join(self.engine_cache[engine], urlhash)
        if os.path.exists(cache_path) and cache:
            with open(cache_path, 'rb') as stream:
                return pickle.load(stream), True
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                html = await resp.text()
                with open(cache_path, 'wb') as stream:
                    pickle.dump(str(html), stream)
                return str(html), False

    def clear(self, engine=None):
        """
        Clear the entire cache either by engine name
        or just all

        :param engine: engine to clear
        """
        if not engine:
            for engine_cache in self.engine_cache.values():
                for root, dirs, files in os.walk(engine_cache):
                    for f in files:
                        os.remove(os.path.join(engine_cache, f))
        else:
            engine_cache = self.engine_cache[engine.lower()]
            for _, _, files in os.walk(engine_cache):
                for f in files:
                    os.remove(os.path.join(engine_cache, f))
