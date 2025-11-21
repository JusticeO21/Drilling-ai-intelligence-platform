from fastapi import APIRouter
from ..schemas import well as well_schema

router = APIRouter()


@router.get("/", response_model=well_schema.WellList)
def get_wells():
    # Sample data - in production, this would query the database
    sample_wells = [
        {"id": 1, "name": "Well A", "depth": 1500.5},
        {"id": 2, "name": "Well B", "depth": 2200.0},
        {"id": 3, "name": "Well C", "depth": 1800.75},
    ]
    return {"wells": sample_wells}
