from typing import Annotated

from fastapi import APIRouter, Query

from core.models.stm.routes import RouteDetail
from core.services.stm.routes import fetch_route_detail

router = APIRouter(prefix="/routes")


@router.get(
    "/{route_id}",
    response_model=RouteDetail,
    summary="Route detail",
    description="Returns real-time vehicle positions and trip updates for a given route.",
)
async def get_route(
    route_id: str,
    include_stop_times: Annotated[bool, Query(description="Include stop_time_updates in trip responses")] = False,
) -> RouteDetail:
    return await fetch_route_detail(route_id, include_stop_times=include_stop_times)
