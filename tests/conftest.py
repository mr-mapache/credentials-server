from pytest import fixture
from fastapi import FastAPI
from fastapi.testclient import TestClient

from server.settings import Settings
from server.connections import Database, Connections
from server.adapters.users import Users
from server.adapters.schemas import Schema
from server.adapters.claims import Authority
from server.adapters.tokens import Tokens
from server.services.auth import Auth
from server.endpoints import auth

@fixture(scope='session')
def settings() -> Settings:
    return Settings()

@fixture(scope='function')
def database(settings: Settings):
    database = Database(settings)
    database.setup()
    transaction = database.connection.begin()
    try:
        yield database
    finally:
        transaction.rollback()
        database.connection.close()
        database.teardown()
 
@fixture(scope='function')
def connections(database: Database):
    with Connections(database) as connections:
        yield connections

@fixture(scope='function')
def users(connections: Connections, settings):
    return Users(connections, settings)

@fixture(scope='function')
def authority():
    return Authority()

@fixture(scope='function')
def tokens(settings):
    return Tokens(settings)

@fixture(scope='function')
def client(users, authority, tokens):
    auth.api.dependency_overrides[auth.service] = lambda: Auth(users, authority, tokens)
    return TestClient(auth.api)