from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class SQLAlchemySettings(BaseSettings):
    host: str = Field(default='localhost')
    port: int = Field(default=5432)
    user: str = Field(...)
    name: str = Field(...)
    password: SecretStr = Field(...)
    model_config = SettingsConfigDict(env_prefix='DATABASE_')

    @property
    def uri(self) -> str:
        return f'postgresql+psycopg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}'

class PasslibSettings(BaseSettings):
    schemes: list[str] = Field(default_factory=lambda: ['bcrypt']) 
    model_config = SettingsConfigDict(env_prefix='CRYPTOGRAPHY_')

class Settings(BaseSettings):
    database: SQLAlchemySettings = Field(default_factory=SQLAlchemySettings)
    cryptography: PasslibSettings = Field(default_factory=PasslibSettings)