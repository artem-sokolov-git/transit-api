from fastapi import APIRouter, Depends

from core.filters.vehicles import VehicleFilter
from core.models.vehicles import VehiclePosition
from core.services.vehicles import fetch_vehicles

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get(
    "",
    response_model=list[VehiclePosition],
    summary="Vehicle positions",
    description="Returns real-time positions of all active STM vehicles from the GTFS-RT feed.",
)
async def get_vehicles(filters: VehicleFilter = Depends()):
    return await fetch_vehicles(filters)
