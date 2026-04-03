import asyncio

from core.filters.stm.trips import TripFilter
from core.filters.stm.vehicles import VehicleFilter
from core.models.stm.routes import RouteDetail
from core.services.stm.trips import fetch_trip_updates
from core.services.stm.vehicles import fetch_vehicles


async def fetch_route_detail(route_id: str, include_stop_times: bool = False) -> RouteDetail:
    vehicles, trips = await asyncio.gather(
        fetch_vehicles(VehicleFilter(route_id=route_id)),
        fetch_trip_updates(TripFilter(route_id=route_id, include_stop_times=include_stop_times)),
    )
    return RouteDetail(route_id=route_id, vehicles=vehicles, trips=trips)
