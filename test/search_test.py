from pprint import pprint

from search import Search

from tmdb import TMDB

t = TMDB()
s = Search(t)
r = s.search_person("jack n")

print(r)
