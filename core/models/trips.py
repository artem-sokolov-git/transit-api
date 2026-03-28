from pydantic import BaseModel


class StopTimeUpdate(BaseModel):
    stop_sequence: int
    stop_id: str
    arrival_time: int | None
    arrival_delay: int | None
    departure_time: int | None
    departure_delay: int | None


class TripUpdate(BaseModel):
    id: str
    trip_id: str
    route_id: str
    direction_id: int
    start_date: str
    stop_time_updates: list[StopTimeUpdate]
