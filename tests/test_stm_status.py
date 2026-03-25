import httpx

from core.config import settings


def test_vehicle_positions(client: httpx.Client):
    response = client.get(settings.position_endpoint)
    assert response.status_code == 200


def test_trip_updates(client: httpx.Client):
    response = client.get(settings.trip_updates_endpoint)
    assert response.status_code == 200


def test_service_status(client: httpx.Client):
    response = client.get(settings.service_status_endpoint)
    assert response.status_code == 200
