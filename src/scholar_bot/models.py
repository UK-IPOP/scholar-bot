from typing import Optional
from pydantic import BaseModel
import csv


class Scholar(BaseModel):
    name: Optional[str]
    citations: Optional[int]
    entries: Optional[int]
    h_index: Optional[int]
    i10_index: Optional[int]

    @classmethod
    def make_scholars(cls) -> list[dict[str, str]]:
        data = []
        with open("data/COPscholars.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(
                    cls(
                        name=row["Name"],
                        citations=row["Citations"],
                        entries=row["Entries"],
                        h_index=row["h-index"],
                        i10_index=row["i10-index"],
                    )
                )
        return data
