from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/ping")
async def healthcheck():
    return {"status": "ok"}
