from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    TRON_API_KEY: str = ""
    TRON_ADDRESS: str = "TQ5JU61ph2w9GmmneM5v8V8Bq9eGHkmq3V"

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    DEBUG_STATUS: bool = True
    SECRET_KEY: str = "your_secret_key"

    class Config:
        env_file = ".env"

settings = Settings()