from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings as PydanticBaseSettings


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"


class DatabaseSettings(BaseSettings):
    user: str = "goods_vault"
    password: SecretStr = "goods_vault"
    host: str = "localhost"
    port: int = 5432
    name: str = "goods_vault"

    @computed_field
    @property
    def url(self) -> str:
        return (f"postgresql+asyncpg://"
                f"{self.user}:{self.password.get_secret_value()}"
                f"@{self.host}:{self.port}/{self.name}")

    class Config:
        env_prefix = "db_"


class GS1RUSettings(BaseSettings):
    captcha_token: SecretStr
    request_timeout: float = 15.0

    class Config:
        env_prefix = "gs1_"


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    gs1: GS1RUSettings = GS1RUSettings()

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    debug: bool = False


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
