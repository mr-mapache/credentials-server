from pytest import fixture
from sqlalchemy import create_engine, Engine
from sqlalchemy import Connection
from sqlalchemy.orm import sessionmaker , Session
from fastapi import FastAPI
from fastapi.testclient import TestClient

from credentials.settings import Settings
from credentials.adapters.schemas import metadata
from credentials.adapters.cryptography import Cryptography
from credentials.adapters.credentials import Credentials
from credentials.endpoints import router, credentials_port, security_port
from credentials.schemas import Credential

@fixture(scope='session')
def settings() -> Settings:
    return Settings()

@fixture(scope='session')
def cryptography(settings: Settings):
    return Cryptography(settings)

@fixture(scope='session')
def engine(settings: Settings):
    engine = create_engine(settings.database.uri)
    yield engine
    engine.dispose()

@fixture(scope='function')
def connection(engine: Engine):
    with engine.connect() as connection:
        transaction = connection.begin()
        metadata.create_all(engine)
        try:
            yield connection
        finally:
            transaction.rollback()
            metadata.drop_all(engine)
            connection.close()

@fixture(scope='function')
def session_maker(connection: Connection):
    yield sessionmaker(bind=connection)

@fixture(scope='function')
def session(session_maker: sessionmaker[Session]):
    with session_maker.begin() as session:
        yield session
        session.commit()

@fixture(scope='function')
def credentials(session: Session, cryptography: Cryptography):
    return Credentials(session, cryptography)

def mock_security(credential: Credential ) -> Credential:
    return credential

@fixture(scope='function')
def client(credentials: Credentials):
    api = FastAPI()
    api.include_router(router)
    api.dependency_overrides[credentials_port] = lambda: credentials
    api.dependency_overrides[security_port] = mock_security
    return TestClient(api)