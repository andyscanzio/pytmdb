from pprint import pprint

from pytmdb.search import Search
from pytmdb.tmdb import TMDB

t = TMDB()
s = Search(t)
r = s.search_person("jack n")

pprint(r)
