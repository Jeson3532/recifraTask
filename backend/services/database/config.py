from pydantic_settings import SettingsConfigDict, BaseSettings
from backend import ROOT_PATH
from pathlib import Path


ENV_FILE = Path(ROOT_PATH) / '.env'


class DBConfig(BaseSettings):
    # данные для подключения
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: str = '5432'
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    # настройки пула подключений
    POOL_SIZE: int = 16
    POOL_OVERFLOW: int = 20
    POOL_TIMEOUT: int = 30

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra='ignore')

    @property
    def base_url(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_url(self, driver: str = 'asyncpg'):
        return (f"postgresql+{driver}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")
