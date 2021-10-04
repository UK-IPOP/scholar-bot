from pydantic import BaseModel
import datetime


class YearCites(BaseModel):
    year: int
    cites: int


class Scholar(BaseModel):
    name: str
    gs_id: str
    affiliation: str
    h_index: int
    i10_index: int
    cited_by: int
    cites_per_year: list[YearCites]
    pub_count: int


class Scholars(BaseModel):
    last_updated: datetime.datetime
    scholars: list[Scholar]
