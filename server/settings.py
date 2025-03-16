from datetime import timedelta
from typing import Annotated
from typing import Optional
from typing import Literal 
from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class PostgreSQLSettings(BaseSettings):
    driver: Annotated[str, Field(default='postgresql+psycopg')]
    host: Annotated[str, Field(default='localhost')]
    port: Annotated[int, Field(default=5432)]
    user: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    url: Annotated[str | None, Field(default=None)]
    password: Annotated[SecretStr, Field(...)]
    model_config = SettingsConfigDict(env_prefix='DATABASE_')

    @property
    def uri(self) -> str:
        if self.url:
            return self.url
        else:
            return f'{self.driver}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}'


class RedisSettings(BaseSettings):
    host: Annotated[str, Field(default='localhost')]
    port: Annotated[int, Field(default=6379)]
    model_config = SettingsConfigDict(env_prefix='CACHE_')

    @property
    def uri(self) -> str:
        return f'redis://{self.host}:{self.port}/0' 

class CORSMiddleware(BaseSettings):
    allow_origins: Annotated[list[str], Field(default_factory=lambda: ['*'])]
    allow_credentials: Annotated[bool, Field(default=True)]
    allow_methods: Annotated[list[str], Field(default_factory=lambda: ['*'])]
    allow_headers: Annotated[list[str], Field(default_factory=lambda: ['*'])]

class SessionsSettings(BaseSettings):
    secret_key: Annotated[SecretStr, Field(...)]
    session_cookie: Annotated[str, Field('session')]
    max_age: Annotated[Optional[int],Field(default=14 * 24 * 60 * 60)]
    path: Annotated[Optional[str], Field(default='/')]
    same_site: Annotated[Literal['lax', 'strict', 'none'], Field(default='lax')]
    https_only: Annotated[bool, Field(default=False)]
    domain: Annotated[Optional[str], Field(default=None)]

    model_config = SettingsConfigDict(env_prefix='SESSIONS_')

class MiddlewareSettings(BaseSettings):
    cors: Annotated[CORSMiddleware, Field(default_factory=CORSMiddleware)]
    sessions: Annotated[SessionsSettings, Field(default_factory=SessionsSettings)]

class Cryptography(BaseSettings):
    key: Annotated[SecretStr, Field(...)]
    schemes: Annotated[list[str], Field(default_factory=lambda: ['bcrypt'])]
    model_config = SettingsConfigDict(env_prefix='CRYPTOGRAPHY_')

class ApiSettings(BaseSettings):
    key: Annotated[SecretStr, Field(...)]
    model_config = SettingsConfigDict(env_prefix='API_')

class Settings(BaseSettings):
    database: Annotated[PostgreSQLSettings, Field(default_factory=PostgreSQLSettings)]
    middleware: Annotated[MiddlewareSettings, Field(default_factory=MiddlewareSettings)] 
    cryptography: Annotated[Cryptography, Field(default_factory=Cryptography)]
    api: Annotated[ApiSettings, Field(default_factory=ApiSettings)] 

def configuration(*args, **kwargs) -> Settings:
    raise NotImplementedError("Override this dependency with a concrete implementation")