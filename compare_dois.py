import csv 
dois = []
with open("papers.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[0] == "DOI":
            pass
        else:
            dois.append(row[0])
yes = []
no = []
with open("papers-livestock.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[0] == "DOI":
            pass
        else:
            if row[0] in dois:
                yes.append(row[0])
                print(row[0])
            else:
                no.append(row[0])

print(len(yes))
print(len(no))
