from crossref_commons.iteration import iterate_publications_as_json
from crossref_commons.relations import get_related
from colorama                   import Fore, Back, Style
from time                       import sleep
import json,csv,sys,os,linecache


cmd = "curl -X GET \"https://api.crossref.org/journals/{}/works?filter=from-pub-date%3A2007&query=meat&order=asc&sort=published\" -H 'User-Agent: ScienceWashing/0.1 (https://greenpeace.org; mailto:ycetinka@greenpeace.org) BasedOnScienceWashing/0.1' > json/journals/{}.json"

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('{}{}:{}{} {}'.format(Fore.RED, filename.split("/")[-1], lineno, Style.RESET_ALL, exc_obj))


def parse_journals(file):
    payload = [["List","Rank","ISSN","Journal Title","Hits"]]
    papers = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        result_count = 0
        for row in csv_reader:
            if line_count <= 0:
                line_count += 1
            else:
                print("{}Querying journal: {}{}".format(Fore.CYAN,Style.RESET_ALL,row[3]))
                succeeded = False

                # check if results are cached
                for issn in row[2].split(", "):
                    fn = "json/journals/{}.json".format(issn)
                    if os.path.exists(fn) and os.stat(fn).st_size > 1:
                        with open(fn) as i:
                            try:
                                j = json.load(i)
                                count = len(j)
                                print("{}Found cached: {}{} {}".format(Fore.GREEN,issn,Style.RESET_ALL,count))
                                result_count += count
                                succeeded = True
                                payload.append([row[0],row[1],issn,row[3],count])

                                for item in j:

                                    funders = " "
                                    if "funder" in list(item.keys()):
                                        funder = []
                                        for f in item["funder"]:
                                            if "DOI" in list(f.keys()):
                                                funder.append(f"{f['name']} ({f['DOI']})")
                                            else:
                                                funder.append(f['name'])
                                        funders = "\n".join(funder)

                                    authors = " "
                                    if "author" in list(item.keys()):
                                        author = []
                                        for a in item["author"]:

                                            if "given" in list(a.keys()) and "family" in list(a.keys()):
                                                nam = f"{a['family']}, {a['given']}"
                                            elif "given" in list(a.keys()):
                                                nam = a["given"]
                                            elif "family" in list(a.keys()):
                                                nam = a["family"]
                                            else:
                                                nam = ""

                                            affies = ""
                                            if "affiliation" in list(a.keys()) and len(a["affiliation"])>0:
                                                affies = " ({})".format("; ".join([x["name"] for x in a["affiliation"]]))

                                            author.append(f"{nam}{affies}")

                                        authors = "\n".join(author)

                                    paper = {
                                                "DOI": item["DOI"],
                                                "Title": "\n".join([x for x in item["title"]]),
                                                "Authors": authors,
                                                "Funders": funders,
                                                "ISSN": issn,
                                                "Journal": "\n".join([x for x in item["container-title"]]),
                                                "Publisher": item["publisher"],
                                                "Published": "-".join([str(x) for x in item["published"]["date-parts"][0]])
                                            }
                                    papers.append(paper)
                            except:
                                succeeded = False
                                PrintException()

                # try accessing results
                for issn in row[2].split(", "):
                    break
                    fn = "json/journals/{}.json".format(issn)
                    try:
                        if not succeeded:
                            sleep(1)
                            f = {
                                    'from-pub-date': "2007",
                                    'issn': issn
                                    }
                            q = {'query.title': 'meat'}
                            cache = []
                            res = iterate_publications_as_json(max_results=9999, filter=f, queries=q)
                            for pub in res:
                                cache.append(pub)
                            with open(fn,"w") as i:
                                i.write(json.dumps(cache, indent=4))
                            if os.path.exists(fn) and os.stat(fn).st_size > 19:
                                succeeded = True
                    except:
                        PrintException()

                line_count += 1

        print("Processed {} lines.".format(line_count - 1))
        print(f"Found {result_count} results.")
        with open('counts.csv', 'w') as file:
            writer = csv.writer(file)
            for row in payload:
                writer.writerow(row)
        

        with open('papers.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(list(papers[0].keys()))
            for paper in papers:
                writer.writerow(list(paper.values()))
        

#journals.query('Cadernos')
parse_journals('misc/journals.csv')
