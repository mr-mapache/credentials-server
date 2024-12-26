from pytest import fixture
from fastapi import FastAPI
from fastapi.testclient import TestClient

from credentials.settings import Settings
from credentials.adapters import Database
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

@fixture(scope='function')
def database(settings: Settings):
    database = Database(settings)
    database.setup()
    metadata.create_all(database.connection)
    yield database
    metadata.drop_all(database.connection)
    database.connection.close()
    database.teardown()

@fixture(scope='function')
def transaction(database: Database):
    transaction = database.connection.begin()
    yield database
    transaction.rollback()
    database.connection.close()

@fixture(scope='function')
def credentials(database: Database, cryptography: Cryptography):
    with database.sessionmaker() as session:
        yield Credentials(session, cryptography)   
        session.commit()

def mock_security(credential: Credential ) -> Credential:
    return credential

@fixture(scope='function')
def client(credentials: Credentials):
    api = FastAPI()
    api.include_router(router)
    api.dependency_overrides[credentials_port] = lambda: credentials
    api.dependency_overrides[security_port] = mock_security
    return TestClient(api)