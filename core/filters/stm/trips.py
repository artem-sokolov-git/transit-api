from dataclasses import dataclass
from typing import Annotated

from fastapi import Query


@dataclass
class TripFilter:
    route_id: Annotated[str | None, Query(description="Filter by route (e.g. 10, 80, 747)")] = None
    direction_id: Annotated[int | None, Query(description="Filter by direction (0 or 1)")] = None
    include_stop_times: Annotated[bool, Query(description="Include stop_time_updates in response")] = False
