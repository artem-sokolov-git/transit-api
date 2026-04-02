from fastapi import HTTPException
from google.transit import gtfs_realtime_pb2

from core.client import stm_client
from core.config import settings
from core.models.stops import StopDeparture


async def fetch_stop_departures(stop_id: str) -> list[StopDeparture]:
    async with stm_client() as client:
        response = await client.get(settings.trip_updates_endpoint)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="STM API error")

    feed = gtfs_realtime_pb2.FeedMessage()  # ty: ignore[unresolved-attribute]
    feed.ParseFromString(response.content)

    departures = []
    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue
        trip = entity.trip_update.trip
        for stu in entity.trip_update.stop_time_update:
            if stu.stop_id != stop_id:
                continue
            departures.append(
                StopDeparture(
                    trip_id=trip.trip_id,
                    route_id=trip.route_id,
                    direction_id=trip.direction_id,
                    stop_sequence=stu.stop_sequence,
                    arrival_time=stu.arrival.time if stu.HasField("arrival") else None,
                    arrival_delay=stu.arrival.delay
                    if stu.HasField("arrival")
                    else None,
                    departure_time=stu.departure.time
                    if stu.HasField("departure")
                    else None,
                    departure_delay=stu.departure.delay
                    if stu.HasField("departure")
                    else None,
                )
            )

    return departures
