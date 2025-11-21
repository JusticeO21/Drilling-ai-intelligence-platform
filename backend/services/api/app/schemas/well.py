from pydantic import BaseModel
from typing import List


class WellBase(BaseModel):
    name: str
    depth: float


class WellCreate(WellBase):
    pass


class Well(WellBase):
    id: int

    class Config:
        from_attributes = True


class WellList(BaseModel):
    wells: List[Well]
