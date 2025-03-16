from typing import Annotated  
from fastapi import Depends
from fastapi import Request
from fastapi import HTTPException, status 
from fastapi import FastAPI
from fastapi import Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates 

from server.schemas import Credentials
from server.schemas import Token
from server.services.auth import Auth, Unauthorized

api = FastAPI() 
bearer = OAuth2PasswordBearer(tokenUrl='token') 
templates = Jinja2Templates(directory='server/templates')
static = StaticFiles(directory='server/static') 

def service() -> Auth:
    raise NotImplementedError("Override this dependency with a concrete implementation")

def credentials(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Credentials:
    return Credentials(username=form.username, password=form.password)

@api.get('/login')
def get_login(request: Request):
    return templates.TemplateResponse('sign-in.html', {"request": request})

@api.post('/token')
def send_login(credentials: Annotated[Credentials, Depends(credentials)], service: Annotated[Auth, Depends(service)]) -> Token:
    try:
        token = service.handle(credentials.username, credentials.password)  
        return Token(access_token=token.payload, token_type='Bearer')

    except Unauthorized:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")