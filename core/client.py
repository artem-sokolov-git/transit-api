import httpx

from core.config import settings


def auth_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(headers={"apikey": settings.token.get_secret_value()})
