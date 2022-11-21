from crossref_commons.iteration import iterate_publications_as_json
from crossref_commons.relations import get_related
from colorama                   import Fore, Back, Style
from time                       import sleep
import json,csv,sys,os,linecache

keywords = []
with open("misc/keywords.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count <= 0:
            line_count += 1
        else:
            keywords.append(row[0].split("+"))

keywords = list(set([i for l in keywords for i in l]))
keywords.sort()

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('{}{}:{}{} {}'.format(Fore.RED, filename.split("/")[-1], lineno, Style.RESET_ALL, exc_obj))


def parse_journals(file):
    payload = [["List","Rank","ISSN","Journal Title","Query","Hits"]]
    for token in keywords:
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
                        #break # HACK
                        fn = f"json/journals/{issn}-{token}.json"
                        if os.path.exists(fn):
                            with open(fn) as f:
                                try:
                                    j = json.load(f)
                                    count = len(j)
                                    print(f"  {Fore.GREEN}Found cached: {issn}{Style.RESET_ALL} {token}, {count}")
                                    result_count += count
                                    payload.append([row[0],row[1],issn,row[3],token,count])
                                    if count > 0:
                                        succeeded = True
                                except:
                                    succeeded = False
                                    PrintException()

                    # try accessing results
                    for issn in row[2].split(", "):
                        fn = f"json/journals/{issn}-{token}.json"
                        if os.path.exists(fn):
                            with open(fn) as f:
                                try:
                                    j = json.load(f)
                                    succeeded = True
                                except:
                                    succeeded = False
                                    PrintException()
                        try:
                            if not succeeded:
                                print(f"  {Fore.YELLOW}Accessing:    {issn}{Style.RESET_ALL} {token}")
                                sleep(1)
                                f = {
                                        'from-pub-date': "2007",
                                        'issn': issn
                                        }
                                q = {'query.title': token}
                                cache = []
                                res = iterate_publications_as_json(max_results=9999, filter=f, queries=q)
                                for pub in res:
                                    cache.append(pub)
                                count = len(cache)
                                result_count += count
                                with open(fn,"w") as i:
                                    i.write(json.dumps(cache, indent=4))
                                if os.path.exists(fn) and os.stat(fn).st_size > 1 and count > 0:
                                    succeeded = True
                        except:
                            PrintException()

                    line_count += 1

            #break #process only first keyword
            print(token)

        print("Processed {} lines.".format(line_count - 1))
        print(f"Found {result_count} results.")
        with open('counts.csv', 'w') as outfile:
            writer = csv.writer(outfile)
            for row in payload:
                writer.writerow(row)
        

#journals.query('Cadernos')
parse_journals('misc/journals.csv')
