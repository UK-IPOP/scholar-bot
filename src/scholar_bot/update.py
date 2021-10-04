import json
from scholarly import scholarly
import csv
import models
import datetime
from pathlib import Path
import pytz

DONE = False
scholar_names = []
success = 0
failed = []

now = datetime.datetime.now(pytz.timezone("US/Eastern"))
current_time = now.strftime("%Y-%m-%d %H:%M:%S")
today = now.strftime("%Y-%m-%d")

with open("./data/scholars.csv", "r") as f:
    csvreader = csv.DictReader(f)
    for row in csvreader:
        scholar_names.append((row["Name"], row["GSID"]))


while not DONE:
    for name, gsid in scholar_names:
        print(f"Updating {name}...")
        try:
            author = scholarly.search_author_id(gsid)
            author_info = scholarly.fill(
                author, sections=["basics", "indices", "counts", "publications"]
            )
        except Exception as e:
            print(e)
            print(f"Failed to update {name}")
            failed.append((name, gsid))
            continue
        clean_author = {
            "name": author_info["name"],
            "gs_id": author_info["scholar_id"],
            "affiliation": author_info["affiliation"],
            "h_index": author_info["hindex"],
            "i10_index": author_info["i10index"],
            "cited_by": author_info["citedby"],
            "cites_per_year": author_info["cites_per_year"],
            "pub_count": len(author_info["publications"]),
        }
        # modularize this json functionality
        # add last_updated functionality
        with open("./data/new.json", "r") as f:
            data = json.load(f)
        data["last_updated"] = current_time
        if today not in data.keys():
            data[today] = dict()
        data[today][clean_author["name"]] = clean_author
        with open("./data/new.json", "w") as f:
            json.dump(data, f, indent=4)

        success += 1
        if success == len(scholar_names):
            DONE = True
            break

print(failed)
