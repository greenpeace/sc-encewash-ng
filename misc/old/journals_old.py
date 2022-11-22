from crossref.restful import Journals, Etiquette
from colorama         import Fore, Back, Style
import json,csv,sys,os,linecache

sw = Etiquette('ScienceWashing', '0.1', 'https://greenpeace.org', 'ycetinka@greenpeace.org')
journals = Journals(etiquette=sw)

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
                    if os.path.exists(fn) and os.stat(fn).st_size > 19:
                        with open(fn) as i:
                            try:
                                j = json.load(i)
                                if j['status'] == 'ok':
                                    count = j["message"]["total-results"]
                                    print("{}Found cached: {}{} {}".format(Fore.GREEN,issn,Style.RESET_ALL,count))
                                    result_count += count
                                    succeeded = True
                                    payload.append([row[0],row[1],issn,row[3],count])
                                    for item in j["message"]["items"]:
                                        paper = {
                                                "doi": item["DOI"],
                                                "title": "; ".join([x for x in item["title"]])
                                                }
                                        print(paper)
                            except:
                                succeeded = False

                # try accessing results
                for issn in row[2].split(", "):
                    fn = "json/journals/{}.json".format(issn)
                    try:
                        if not succeeded:
                            content = journals.works(issn).query('meat').filter(from_pub_date='2007')
                            result = os.system(cmd.format(issn,issn))
                            count = 0
                            if os.stat(fn).st_size > 19:
                                with open(fn) as i:
                                    j = json.load(i)
                                    if j['status'] == 'ok':
                                        count = j["message"]["total-results"]
                                        succeeded = True
                                        print("{} {}{}".format(result,Fore.GREEN,count,Style.RESET_ALL))
                    except:
                        PrintException()
                line_count += 1
                break

        print(f'Processed {line_count} lines.')
        print(f'Found {result_count} results.')
        with open('counts.csv', 'w') as file:
            writer = csv.writer(file)
            for row in payload:
                writer.writerow(row)

#journals.query('Cadernos')
parse_journals('misc/journals.csv')
