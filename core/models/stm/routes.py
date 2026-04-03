from pydantic import BaseModel

from core.models.stm.trips import TripUpdate
from core.models.stm.vehicles import VehiclePosition


class RouteDetail(BaseModel):
    route_id: str
    vehicles: list[VehiclePosition]
    trips: list[TripUpdate]
