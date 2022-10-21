from sci_dl     import dl_by_doi
from colorama   import Fore, Back, Style
from time       import sleep
import csv, os

config = { 'base_url': 'https://sci-hub.ru', 'retries': 5, 'use_proxy': False }
failed = []
with open("papers.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[0] != "DOI": 
            journal = "_".join(str.lower(row[5]).split(" "))
            title = "-".join(str.lower(row[0]).split("/"))
            if not os.path.exists(f"pdfs/{journal}"):
                os.makedirs(f"pdfs/{journal}")
            fn = "pdfs/{}/{}.pdf".format(journal,title)
            if not os.path.exists(fn):
                sleep(2)
                try:
                    pub = dl_by_doi(row[0],config)
                    with open(fn, "wb") as fp:
                        fp.write(pub.content)
                    print(f"{Fore.GREEN}{fn}{Style.RESET_ALL}")
                except Exception as err:
                    print(f"{Fore.RED}{err}{Style.RESET_ALL} ({journal})")
                    failed.append({
                            "DOI": row[0],
                            "Title": row[1],
                            "Journal": row[5]
                        })
            else:
                print(f"{Fore.CYAN}{fn}{Style.RESET_ALL}")
print(len(failed))


