from crossref_commons.iteration import iterate_publications_as_json
from crossref_commons.relations import get_related

from sci_dl import dl_by_doi

import logging, pprint, json, os

logging.basicConfig( level=logging.DEBUG)
rows = 100

filter = {
        'from-pub-date': "2007",
        'issn': "17586798"
        }

queries = {'query.title': 'meat'}

cachefile = "./json/test.json"
cache = []
if os.path.exists(cachefile):
    with open(cachefile,"r") as f:
        cache = json.load(f)

def query(q=queries,f=filter):

    if len(cache) == 0 or True:
        res = iterate_publications_as_json(max_results=rows, filter=f, queries=q)
        print("OK")
        for pub in res:
            cache.append(pub)
        with open(cachefile, "w") as o:
            o.write(json.dumps(cache, indent=4))

    return cache

def related(doi):

    if len(cache) == 0 or True:
        pub = get_related(doi)
        cache.append(pub)
        print("OK")
        with open(cachefile, "w") as o:
            o.write(json.dumps(cache, indent=4))

    return cache

#query()

"""
config = { 'base_url': 'https://sci-hub.ru', 'retries': 5, 'use_proxy': False }
#pub = dl_by_doi("10.1093/jas/skaa172",config) # Culture, meat, and cultured meat
pub = dl_by_doi("10.1016/j.soscij.2007.11.001",config)
print(pub.__class__)
with open('pdfs/yyy.pdf', 'wb') as fp:
    fp.write(pub.content)

"""
cm = {}
with open("./culturemeat.json","r") as f:
    cm = json.load(f)

refs = []
for ref in cm["reference"]:
    if "DOI" in ref.keys():
        refs.append(ref["DOI"])

fd = {}
with open("./refs_funded.json","r") as f:
    fd = json.load(f)

frs = {}
for pub in fd:
    frs[pub["DOI"]] = [[],[]]
    for funders in pub["author"]:
        if isinstance(funders,list):
            for funder in funders:
                name = ""
                if "family" in funder.keys():
                    name += funder["family"]
                if "given" in funder.keys():
                    name += ", "+funder["given"]
                if "affiliation" in funder.keys():
                    for affil in funder["affiliation"]:
                        frs[pub["DOI"]][1].append(affil["name"])
                frs[pub["DOI"]][0].append(name)
        else:
            name = ""
            if "family" in funders.keys():
                name += funders["family"]
            if "given" in funders.keys():
                name += ", "+funders["given"]
            if "affiliation" in funders.keys():
                for affil in funders["affiliation"]:
                    frs[pub["DOI"]][1].append(affil["name"])
            frs[pub["DOI"]][0].append(name)
    print(pub["title"][0])
    print(frs[pub["DOI"]])

#query({},{"relation.type":"is-referenced-by","relation.object":"10.1093/jas/skaa172"})
#query({},{"has-funder:1,doi:"+",doi:".join(refs)})

