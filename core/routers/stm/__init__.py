from fastapi import APIRouter

from core.routers.stm import routes, stops, trips, vehicles

router = APIRouter(prefix="/stm", tags=["stm"])

router.include_router(vehicles.router)
router.include_router(trips.router)
router.include_router(stops.router)
router.include_router(routes.router)
