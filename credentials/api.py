from fastapi import FastAPI
from credentials.settings import Settings
from credentials.adapters import Database
from credentials.adapters.cryptography import Cryptography
from credentials.adapters.credentials import Credentials
from credentials.endpoints import router, credentials_port, security_port
from credentials.security import basic_security_adapter

settings = Settings()
database = Database(settings)
cryptography = Cryptography(settings)

def lifespan(api: FastAPI):
    database.setup()
    yield
    database.teardown()

def credentials_adapter():
    with database.sessionmaker() as session:
        yield Credentials(session, cryptography)
        session.commit()

api = FastAPI(lifespan=lifespan)
api.include_router(router)
api.dependency_overrides[credentials_port] = credentials_adapter
api.dependency_overrides[security_port] = basic_security_adapter