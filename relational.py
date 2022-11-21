from external.graphcommons.graphcommons import GraphCommons, Signal
from colorama                            import Fore, Back, Style
from time                               import sleep
import csv

gc = GraphCommons("sk_qb99ugcQWl7Muz0CPtZmqQ")
gids = ["611562b2-c57d-4492-8b5c-99a7e39741c6","7fea51a9-2d0c-4a03-ade6-184645233c03","11a72428-e3c7-4a35-8453-dfdb70ffb9a4"]
graphs = []
lists = []
with open("misc/papers.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count <= 0:
            line_count += 1
        else:
            lists.append(row[8])
lists = list(set(lists))
lid = 0
for lst in lists:
    graph = gc.clear_graph(gids[lid])
    print(f"{Fore.CYAN}{graph['name']}{Style.RESET_ALL}")
    ss = [
            Signal(
                    action = "nodetype_create",
                    color = "#CC0000",
                    description = None,
                    hide_name = None,
                    image = None,
                    image_as_icon = True,
                    name = "Paper",
                    name_alias = None,
                    properties = [],
                    size = "metric_degree",
                    size_limit = 48
                  )
         ]
    duplies = {
            "authors": [],
            "affies":  [],
            "author_affies": []
            }


    nodes = 0
    with open("misc/papers.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        header = []
        for row in csv_reader:
            if line_count <= 0:
                header = row
                line_count += 1
            elif row[8] == lst:
                nodes += 1
                ss.append(Signal(
                        action =        "node_create",
                        name =          row[1],
                        type =          "Paper",
                        description =   row[0]
                    ))

                # Authors
                for author in row[3].split("\n"):
                    name = author
                    affies = []
                    if "(" in author and ")" in author:
                        name = author[0:author.find("(")-1]
                        affies = author[author.find("(")+1:author.find(")")].split("; ")
                    name = name.strip()

                    if name == "":
                        continue

                    if name not in duplies["authors"]:
                        duplies["authors"].append(name)
                        nodes += 1
                        ss.append(Signal(
                                action =        "node_create",
                                name =          name,
                                type =          "Author"
                            ))

                    ss.append(Signal(
                            action =        "edge_create",
                            from_name =     name,
                            from_type =     "Author",
                            to_name =       row[1],
                            to_type =       "Paper",
                            name =          "Wrote",
                        ))

                    for affie in affies:
                        if affie not in duplies["affies"]:
                            duplies["affies"].append(affie)
                            nodes += 1
                            ss.append(Signal(
                                    action =        "node_create",
                                    name =          affie,
                                    type =          "Institution"
                                ))

                        if f"{name}-{affie}" not in duplies["author_affies"]:
                            duplies["author_affies"].append(f"{name}-{affie}")
                            ss.append(Signal(
                                    action =        "edge_create",
                                    from_name =     name,
                                    from_type =     "Author",
                                    to_name =       affie,
                                    to_type =       "Institution",
                                    name =          "Affiliated"
                                ))

                # Funders
                for funder in row[4].split("\n"):
                    name = funder
                    if "(" in funder and ")" in funder:
                        name = funder[0:funder.find("(")-1]
                        doi = funder[funder.find("(")+1:funder.find(")")].split("; ")
                    name = name.strip()

                    if name == "":
                        continue

                    if name not in duplies["affies"]:
                        duplies["affies"].append(name)
                        nodes += 1
                        ss.append(Signal(
                                action =        "node_create",
                                name =          name,
                                type =          "Institution"
                            ))

                    ss.append(Signal(
                            action =        "edge_create",
                            from_name =     name,
                            from_type =     "Institution",
                            to_name =       row[1],
                            to_type =       "Paper",
                            name =          "Funded"
                        ))
                line_count += 1

            if line_count > 120 and False:
                break
    print(nodes)
    sent = 0
    for batch in [ss[i:i + 1000] for i in range(0, len(ss), 1000)]:
        print(f"{sent} / {len(ss)}")
        try:
            gc.update_graph(
                id=gids[lid],
                signals=batch
            )
        except Exception as err:
            print(err)
        sent += len(batch)
        sleep(1)

    print(f"{sent} / {len(ss)}")
    lid += 1
