from bs4 import BeautifulSoup
import csv
import json

school_ids_web = {}
school_ids_csv = {}

# scrape schulnummern + links from website
with open("schule_suchen.html", "r") as f:
    soup = BeautifulSoup(f, "html.parser")

    for resultTile in soup.find_all("a", {"class": "links fl"}):
        id = resultTile["href"].split("=")[-1]
        school_ids_web[id] = resultTile["href"]

    with open("output_schule_suchen.txt", "w") as w:
        w.write(json.dumps(school_ids_web))

# scrape schulnummern + infos from csv
with open("schuldaten.csv", "r") as f:
    reader = csv.reader(f, delimiter=";")
    next(reader)
    next(reader)
    for row in reader:
        id = row[0]
        school_ids_csv[id] = row

    with open("output_csv.txt", "w") as w:
        w.write(json.dumps(school_ids_csv))

# in web but not in csv
for web_i in school_ids_web:
    if web_i not in school_ids_csv:
        print("Not in csv " + web_i)

# in csv but not in web
for csv_i in school_ids_csv:
    if csv_i not in school_ids_web:
        if str(csv_i)[0] != "6":
            if school_ids_csv[csv_i][-5] != "2":
                # all start with 6 or 9, so no listing or closed school
                # https://www.schulministerium.nrw.de/BiPo/OpenData/Schuldaten/key_schulbetriebsschluessel.csv
                print(school_ids_csv[csv_i][-5], school_ids_csv[csv_i])
