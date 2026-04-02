from fastapi import APIRouter

from core.models.stops import StopDeparture
from core.services.stops import fetch_stop_departures

router = APIRouter(prefix="/stops", tags=["stops"])


@router.get(
    "/{stop_id}/departures",
    response_model=list[StopDeparture],
    summary="Stop departures",
    description="Returns real-time departures for a given stop from the GTFS-RT trip updates feed.",
)
async def get_stop_departures(stop_id: str) -> list[StopDeparture]:
    return await fetch_stop_departures(stop_id)
