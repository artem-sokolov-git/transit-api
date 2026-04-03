from pydantic import BaseModel


class StopDeparture(BaseModel):
    trip_id: str
    route_id: str
    direction_id: int
    stop_sequence: int
    arrival_time: int | None
    arrival_delay: int | None
    departure_time: int | None
    departure_delay: int | None
