import json
from itertools import chain

file_path="data/slug_search_terms.json"

with open(file_path) as f:
    slug_queries = json.load(f)

def get_slugs(query):
    return query.split("$")

def flatten(l):
    return list(chain.from_iterable(l))

def get_related_terms(query):
    slugs = get_slugs(query)
    cand_sem = [slug_queries[s] for s in slugs if slug_queries.get(s)]
    res = sorted(flatten(cand_sem), key=lambda x: x["comb"], reverse=True)
    res = [r["key"] for  r in res]
    return res
