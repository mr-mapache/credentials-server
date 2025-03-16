from typing import Annotated
from fastapi import FastAPI 
from fastapi import Depends   
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from server.settings import Settings
from server.connections import Database, Connections
from server.middleware import Middleware, SessionMiddleware, CORSMiddleware
from server.adapters.users import Users
from server.adapters.claims import Authority
from server.adapters.tokens import Tokens
from server.services.auth import Auth
from server.endpoints import auth

settings = Settings()
database = Database(settings) 
middleware = [
    Middleware(CORSMiddleware, settings.middleware.cors.model_dump()),
    Middleware(SessionMiddleware, settings.middleware.sessions.model_dump())
]
 
authority = Authority()
tokens = Tokens(settings)

templates = Jinja2Templates(directory="server/templates")
static = StaticFiles(directory="server/static")

def lifespan(api):
    database.setup() 
    yield 
    database.teardown()

def repository():
    with Connections(database) as connections:
        return Users(connections, settings)

def auth_service(users: Annotated[Users, Depends(repository)]):
    return Auth(users, authority, tokens)

auth.api.dependency_overrides[auth.service] = auth_service

api = FastAPI(lifespan=lifespan, middleware=middleware) 
api.mount('/auth', auth.api)