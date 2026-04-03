from fastapi import APIRouter

from core.routers.stm import stops, trips, vehicles

router = APIRouter(prefix="/stm", tags=["stm"])

router.include_router(vehicles.router)
router.include_router(trips.router)
router.include_router(stops.router)
