from crossref.restful import Journals, Etiquette
from colorama         import Fore, Back, Style
from time             import sleep
import json,csv,sys,os,linecache

sw = Etiquette('ScienceWashing', '0.1', 'https://greenpeace.org', 'ycetinka@greenpeace.org')
journals = Journals(etiquette=sw)

rest_command = "curl -X GET \"https://api.crossref.org/journals/{}/works?filter=from-pub-date%3A2007&query=meat&order=asc&sort=published&cursor={}\" -H 'User-Agent: ScienceWashing/0.1 (https://greenpeace.org; mailto:ycetinka@greenpeace.org) BasedOnScienceWashing/0.1' > json/journals/{}-{}.json"

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('{}{}:{}{} {}'.format(Fore.RED, filename.split("/")[-1], lineno, Style.RESET_ALL, exc_obj))

forever = True
cursor = "*"

def parse_journals(file):
    global forever
    global cursor
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
                cursor = "*"

                # check if results are cached
                for issn in row[2].split(", "):
                    total = 0
                    count = 0
                    index = 0

                    while forever:
                        fn = "json/journals/{}-{}.json".format(issn,index)
                        if os.path.exists(fn) and os.stat(fn).st_size > 128:
                            i = open(fn)
                            try:
                                j = json.load(i)
                                if j['status'] == 'ok':
                                    total = j["message"]["total-results"]
                                    count += len(j["message"]["items"])
                                    result_count += total



                                    # analyse papers here
                                    for item in j["message"]["items"]:
                                        paper = {
                                                "doi": item["DOI"],
                                                "title": "; ".join([x for x in item["title"]])
                                                }
                                        #print(paper)



                                    if total > count:
                                        index += 1
                                        print("{}Found cached: {}{} {}/{} {}, {}".format(Fore.YELLOW,issn,Style.RESET_ALL,count,total,forever,index))
                                        cursor = j["message"]["next-cursor"]
                                        succeeded = False
                                    else:
                                        succeeded = True
                                        forever = False
                                        print("{}Found cached: {}{} {}/{} {}, {}".format(Fore.GREEN ,issn,Style.RESET_ALL,count,total,forever,index))
                                        payload.append([row[0],row[1],issn,row[3],total])

                            except:
                                succeeded = False
                                PrintException()

                        else:
                            succeeded = False
                            break
                        sleep(0.1)
                    break # issn for loop

                # try accessing results
                for issn in row[2].split(", "):
                    forever = True
                    if not succeeded:
                        #content = journals.works(issn).query('meat').filter(from_pub_date='2007')
                        index = 0
                        count = 0
                        total = 0
                        result = ""

                        while forever:
                            fn = "json/journals/{}-{}.json".format(issn,index)
                            tries = 3
                            while not os.path.exists(fn) or os.stat(fn).st_size <= 128 and tries > 0:
                                try:
                                    sleep(1)
                                    print("{}Accessing: {}{} file {}".format(Fore.GREEN,issn,Style.RESET_ALL,fn))
                                    print(rest_command.format(issn,cursor,issn,index))
                                    result = os.system(rest_command.format(issn,cursor,issn,index))
                                    tries -= 1
                                except:
                                    PrintException()

                            with open(fn) as i:
                                try:
                                    j = json.load(i)
                                    if j['status'] == 'ok':
                                        total = j["message"]["total-results"]
                                        count += len(j["message"]["items"])
                                        if total > count:
                                            index += 1
                                            cursor = j["message"]["next-cursor"]
                                            print("{}{}/{}{} {}".format(result,Fore.YELLOW,count,total,Style.RESET_ALL,cursor))
                                        else:
                                            succeeded = True
                                            print("{}{}/{}{}".format(result,Fore.GREEN ,count,total,Style.RESET_ALL))
                                            forever = False

                                except:
                                    PrintException()

                            sleep(0.5)
                            break
                    break # issn for loop

                line_count += 1
                #break

        print("Processed {} lines.".format(line_count - 1))
        print(f"Found {result_count} results.")
        with open('counts.csv', 'w') as file:
            writer = csv.writer(file)
            for row in payload:
                writer.writerow(row)

#journals.query('Cadernos')
parse_journals('misc/journals.csv')
