# STM Montreal API — Portfolio Project

## Идея
REST API поверх открытых данных STM (Société de transport de Montréal), к которому можно подключить любой фронтенд — Telegram-бот, веб-карту, мобильное приложение.

## Источники данных

| Тип                      | URL                                                          | Доступ          |
| ------------------------ | ------------------------------------------------------------ | --------------- |
| GTFS Static (расписание) | `https://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip` | Без регистрации |
| GTFS-RT TripUpdates      | `https://api.stm.info/pub/od/gtfs-rt/ic/v2/tripUpdates`      | API-ключ        |
| GTFS-RT VehiclePositions | `https://api.stm.info/pub/od/gtfs-rt/ic/v2/vehiclePositions` | API-ключ        |
| Service Status           | `https://api.stm.info/pub/od/i3/v2/messages/etatservice`     | API-ключ        |

Регистрация: https://portail.developpeurs.stm.info/apihub

## Стек

- **FastAPI** — REST API
- **Granian** — ASGI-сервер (замена uvicorn)
- **httpx** — HTTP-клиент для запросов к STM API
- **pydantic-settings** — конфигурация через переменные окружения
- **uv** — менеджер пакетов
- **pytest** — интеграционные тесты
- **ruff** — линтер и форматтер
- **Docker / Docker Compose** — контейнеризация

## Структура проекта

```
stm-api/
├── core/
│   ├── __init__.py
│   ├── config.py           # pydantic-settings: токен, URL endpoints
│   └── main.py             # FastAPI app, /ping healthcheck
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # pytest fixtures (httpx.Client с apikey)
│   └── test_stm_status.py  # интеграционные тесты STM API
├── .env                    # переменные окружения (TOKEN)
├── .pre-commit-config.yaml # ruff + стандартные хуки
├── docker-compose.yaml
├── Dockerfile
├── Makefile
├── pyproject.toml
└── uv.lock
```

## Конфигурация

Настройки читаются из `.env` через `pydantic-settings`:

```python
# core/config.py
class Settings(ApplicationSettings, GTFSRealtimeSettings, STMServiceStatusSettings):
    pass

settings = Settings()
```

`.env`:
```dotenv
TOKEN=your_api_key_here
```

Переменная `TOKEN` используется как `apikey` в заголовках запросов к STM API.

## Доступные команды (Makefile)

```
make run       # Собрать и запустить контейнер
make down      # Остановить контейнер
make clear     # Остановить и удалить volumes
make logs      # Логи контейнера
make check     # ruff lint + format check + ty check
make tests     # Запустить pytest
make rebuild   # Пересобрать проект с нуля
```

## Запуск

```bash
# Локально
uv run granian --interface asgi --host 0.0.0.0 --port 8000 core.main:app

# Docker
make run
```

Healthcheck: `GET /ping` → `{"status": "ok"}`

## Планируемые API Endpoints

```
GET /stops/nearby?lat=45.508&lon=-73.587&radius=500
GET /stops/{stop_id}/departures?limit=5
GET /vehicles/positions?route_id=69
GET /routes?search=69
```

## Планируемая структура проекта

```
core/
├── main.py
├── config.py
├── gtfs/
│   ├── static.py       # загрузка и парсинг GTFS ZIP
│   ├── realtime.py     # запросы к STM GTFS-RT
│   └── models.py       # dataclasses: Stop, Departure, Route
├── api/
│   ├── stops.py        # GET /stops/nearby, GET /stops/{id}/departures
│   ├── routes.py       # GET /routes/{id}
│   └── vehicles.py     # GET /vehicles/positions
└── services/
    ├── stops.py        # find_nearby_stops(), get_departures()
    └── cache.py        # in-memory кэш
```

## Статус

- [x] Зарегистрироваться на portail.developpeurs.stm.info
- [x] Инициализировать проект (`uv init stm-api`)
- [x] Конфигурация через pydantic-settings
- [x] Docker / Docker Compose с healthcheck
- [x] Интеграционные тесты GTFS-RT и Service Status
- [ ] Парсинг GTFS Static (stops, routes, trips)
- [ ] Подключение GTFS-RT (tripUpdates, vehiclePositions)
- [ ] Endpoint `/stops/nearby`
- [ ] Endpoint `/stops/{id}/departures`
- [ ] Telegram-бот (отдельный репо)

## Референсы

- [nyctrains](https://github.com/arrismo/nyctrains) — аналогичная архитектура для MTA Нью-Йорка
- [gtfs_kit docs](https://github.com/mrcagney/gtfs_kit) — парсинг GTFS Static
- [morningcashee.com](https://www.morningcashee.com/blog/2024/06/13/getting-realtime-transit-data/) — туториал по STM GTFS-RT на Python
