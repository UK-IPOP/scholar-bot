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
failed = set()
tries = 0

now = datetime.datetime.now(pytz.timezone("US/Eastern"))
current_time = now.strftime("%Y-%m-%d %H:%M:%S")
today = now.strftime("%Y-%m-%d")

with open("./data/scholars.csv", "r") as f:
    csvreader = csv.DictReader(f)
    for row in csvreader:
        scholar_names.append((row["Name"], row["GSID"]))


while not DONE:
    for name, gsid in scholar_names:
        if name in failed:
            print(f"Retrying {name}...")
        else:
            print(f"Updating {name}...")
        try:
            author = scholarly.search_author_id(gsid)
            author_info = scholarly.fill(
                author,
                sections=["basics", "indices", "counts", "publications"],
            )
        except Exception as e:
            print(e)
            print(f"Failed to update {name}")
            failed.add(name)
            continue
        pubs = author_info.get("publications", None)
        clean_author = {
            "name": name.title(),
            "gs_id": author_info.get("scholar_id", None),
            "affiliation": author_info.get("affiliation", None),
            "h_index": author_info.get("hindex", None),
            "i10_index": author_info.get("i10index", None),
            "cited_by": author_info.get("citedby", None),
            "pub_count": len(pubs) if pubs else None,
            "cites_per_year": author_info.get("cites_per_year", None),
        }
        # modularize this
        with open("./data/scholar_data.csv", "a") as f:
            csvwriter = csv.DictWriter(
                f,
                fieldnames=[
                    "name",
                    "gs_id",
                    "affiliation",
                    "h_index",
                    "i10_index",
                    "cited_by",
                    "pub_count",
                    "year",
                    "cites",
                    "day_added",
                ],
            )
            for year, cite_count in clean_author["cites_per_year"].items():
                info = dict(
                    name=clean_author["name"],
                    gs_id=clean_author["gs_id"],
                    affiliation=clean_author["affiliation"],
                    h_index=clean_author["h_index"],
                    i10_index=clean_author["i10_index"],
                    cited_by=clean_author["cited_by"],
                    pub_count=clean_author["pub_count"],
                    year=year,
                    cites=cite_count,
                    day_added=today,
                )
                csvwriter.writerow(info)

        success += 1
        if success == len(scholar_names):
            DONE = True
            break
    tries += 1
    if tries == 3:
        print("Reached 3rd retry loop, exiting...")
        day = datetime.date.today().strftime("%Y-%m-%d")
        with open(f"./data/failed_{day}.csv", "w") as f:
            csvwriter = csv.DictWriter(f, fieldnames=["name", "gsid"])
            csvwriter.writeheader()
            for name, gsid in scholar_names:
                if name in failed:
                    csvwriter.writerow({"name": name, "gsid": gsid})
        break


print("Done.")
