from typing import Annotated

from fastapi import FastAPI 
from fastapi import Depends
from fastapi import Security
from fastapi import HTTPException, status
from fastapi import Header
from server.settings import Settings
from server.connections import Database, Connections
from server.middleware import Middleware, CORSMiddleware, SessionMiddleware 
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

def lifespan(api):
    database.setup() 
    yield 
    database.teardown()

def repository():
    with Connections(database) as connections:
        return Users(connections, settings)

def service(users: Annotated[Users, Depends(repository)]):
    return Auth(users, authority, tokens)
 
def security(x_key: Annotated[str, Header(...)]):
    if not x_key == settings.api.key.get_secret_value():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")

api = FastAPI(root_path='/api', lifespan=lifespan, middleware=middleware) 
api.include_router(auth.router, dependencies=[Security(security)])
api.dependency_overrides[auth.service] = service 