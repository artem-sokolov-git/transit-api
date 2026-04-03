from fastapi import APIRouter, Depends

from core.filters.stm.trips import TripFilter
from core.models.stm.trips import TripUpdate
from core.services.stm.trips import fetch_trip_updates

router = APIRouter(prefix="/trips")


@router.get(
    "",
    response_model=list[TripUpdate],
    summary="Trip updates",
    description="Returns real-time trip updates for all active STM trips from the GTFS-RT feed.",
)
async def get_trip_updates(filters: TripFilter = Depends()):
    return await fetch_trip_updates(filters)
