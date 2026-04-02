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
- **ty** — проверка типов
- **Docker / Docker Compose** — контейнеризация

## Архитектура

```
router → service → STM GTFS-RT (protobuf) → Pydantic models → фильтрация
```

- **Routers** (`core/routers/`) — HTTP-слой, принимают query params через `Depends()`
- **Services** (`core/services/`) — бизнес-логика, async HTTP-запросы к STM API
- **Models** (`core/models/`) — Pydantic-модели для ответов
- **Filters** (`core/filters/`) — dataclass-зависимости для query params
- **Client** (`core/client.py`) — `stm_client()` возвращает `httpx.AsyncClient` с pre-injected `apikey`

## Доступные команды (Makefile)

```
make run       # Собрать и запустить контейнер
make down      # Остановить контейнер
make logs      # Логи контейнера
make rebuild   # Пересобрать проект с нуля
make check     # ruff lint + format check + ty check
make tests     # Запустить pytest
```

## Запуск

```bash
# Локально
uv run granian --interface asgi --host 0.0.0.0 --port 8000 core.main:app

# Docker
make run
```

## Тесты

Интеграционные тесты — обращаются к реальному STM API. Требуется валидный `.env` с `TOKEN`.

```bash
make tests
# или отдельный тест:
uv run pytest tests/test_stm_status.py::test_vehicle_positions
```

## Деплой

Push в `main` → GitHub Actions → сборка Docker-образа → push в GitHub Container Registry (`ghcr.io`).
Образ тегируется как `latest` и `sha-<commit>`.

## Roadmap

**Готово**
- [x] Конфигурация через pydantic-settings, Docker / Docker Compose с healthcheck
- [x] HTTP-клиент (`httpx.AsyncClient`) с pre-injected apikey
- [x] Интеграционные тесты (реальный STM API)
- [x] `GET /vehicles` — позиции транспорта, фильтрация по `route_id` и `direction_id`
- [x] `GET /trips` — обновления рейсов, фильтрация по маршруту и направлению
- [x] CI/CD: GitHub Actions → GHCR

**Следующие шаги**
- [ ] `GET /stops/{stop_id}/departures` — ближайшие отправления с остановки
- [ ] `GET /stops` — список остановок из GTFS Static
- [ ] Кэширование GTFS-RT ответов (TTL ~30s) для снижения нагрузки на STM API
- [ ] `GET /routes/{route_id}` — агрегированный ответ: позиции + рейсы по маршруту

## Референсы

- [nyctrains](https://github.com/arrismo/nyctrains) — аналогичная архитектура для MTA Нью-Йорка
- [gtfs_kit docs](https://github.com/mrcagney/gtfs_kit) — парсинг GTFS Static
- [morningcashee.com](https://www.morningcashee.com/blog/2024/06/13/getting-realtime-transit-data/) — туториал по STM GTFS-RT на Python
