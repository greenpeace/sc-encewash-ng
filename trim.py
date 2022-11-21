from colorama                   import Fore, Back, Style
import json,csv,sys,os,linecache

rejected = []
with open("misc/rejected.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count <= 0:
            line_count += 1
        else:
            rejected.append(row[0])

keywords = []
with open("misc/keywords.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count <= 0:
            line_count += 1
        else:
            keywords.append(row[0])

keyws = list(set([i for l in keywords for i in l.split("+")]))
keyws.sort()

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('{}{}:{}{} {}'.format(Fore.RED, filename.split("/")[-1], lineno, Style.RESET_ALL, exc_obj))

def trim_journals(file):
    papers = []
    tois = {}
    issns = {}
    names = {}
    for token in keyws:
        tois[token] = []
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            result_count = 0
            for row in csv_reader:
                if line_count <= 0:
                    line_count += 1
                else:
                    succeeded = False

                    # check if results are cached
                    for issn in row[2].split(", "):
                        fn = f"json/journals/{issn}-{token}.json"
                        if os.path.exists(fn) and os.stat(fn).st_size > 1:
                            with open(fn) as i:
                                try:
                                    j = json.load(i)
                                    count = len(j)
                                    for item in j:
                                        if item["DOI"] not in rejected:
                                            tois[token].append(item["DOI"])
                                            issns[item["DOI"]] = issn
                                            names[item["DOI"]] = row[3]
                                            result_count += 1
                                    succeeded = True
                                except:
                                    succeeded = False
                                    PrintException()
                    line_count += 1

            print(f"\r{Fore.CYAN}{token}:{Style.RESET_ALL} {result_count}")
    trimmed = {}
    total = 0
    for token in keywords:
        tokes = token.split("+") 
        if len(tokes) == 1:
            trimmed[token] = tois[token]
        else:
            tok = tois[tokes.pop()]
            for toke in tokes:
                tok = set(tok) & set(tois[toke])
            trimmed[token] = tok
        total += len(trimmed[token])
        print(f"{Fore.GREEN}{token}{Style.RESET_ALL}: {len(trimmed[token])}")
    print(f"{Fore.RED}Total:{Style.RESET_ALL}: {total}")

    papers = {}
    for token in trimmed:
        for paper in trimmed[token]:
            if paper in papers:
                papers[paper].append(token)
            else:
                papers[paper] = [token]


    with open('misc/tokens.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["DOI","Keywords","ISSN","Journal"])
        for doi in papers:
            writer.writerow([doi,", ".join(papers[doi]),issns[doi],names[doi]])

#journals.query('Cadernos')
trim_journals('misc/journals.csv')
