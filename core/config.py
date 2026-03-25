from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class ApplicationSettings(EnvBaseSettings):
    token: SecretStr


class GTFSRealtimeSettings(EnvBaseSettings):
    gtfs_url: str = "https://api.stm.info/pub/od/gtfs-rt/ic/v2"

    @property
    def position_endpoint(self) -> str:
        return f"{self.gtfs_url}/vehiclePositions"

    @property
    def trip_updates_endpoint(self) -> str:
        return f"{self.gtfs_url}/tripUpdates"


class STMServiceStatusSettings(EnvBaseSettings):
    status_url: str = "https://api.stm.info/pub/od/i3/v2/messages"

    @property
    def service_status_endpoint(self) -> str:
        return f"{self.status_url}/etatservice"


class Settings(ApplicationSettings, GTFSRealtimeSettings, STMServiceStatusSettings):
    pass


settings = Settings()  # ty:ignore[missing-argument]
