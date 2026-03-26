from fastapi import APIRouter, HTTPException
from google.transit import gtfs_realtime_pb2

from core.client import stm_client
from core.config import settings
from core.models.vehicles import VehiclePosition

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("", response_model=list[VehiclePosition])
async def get_vehicles():
    async with stm_client() as client:
        response = await client.get(settings.position_endpoint)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="STM API error")

    feed = gtfs_realtime_pb2.FeedMessage()  # ty: ignore[unresolved-attribute]
    feed.ParseFromString(response.content)

    return [
        VehiclePosition(
            id=entity.id,
            route_id=entity.vehicle.trip.route_id,
            direction_id=entity.vehicle.trip.direction_id,
            trip_id=entity.vehicle.trip.trip_id,
            latitude=entity.vehicle.position.latitude,
            longitude=entity.vehicle.position.longitude,
            bearing=entity.vehicle.position.bearing,
            speed=entity.vehicle.position.speed,
            current_status=entity.vehicle.current_status,
            stop_id=entity.vehicle.stop_id,
            occupancy_status=entity.vehicle.occupancy_status,
            timestamp=entity.vehicle.timestamp,
        )
        for entity in feed.entity
    ]
