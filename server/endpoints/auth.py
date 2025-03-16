from uuid import uuid4
from typing import Annotated
from fastapi import APIRouter
from fastapi import Response
from fastapi import Depends
from fastapi import Request
from fastapi import HTTPException, status
from fastapi import Security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

from server.schemas import Credentials
from server.schemas import Token
from server.services.auth import Auth, Unauthorized

router = APIRouter(prefix='/auth') 
bearer = OAuth2PasswordBearer(tokenUrl='auth/token') 

def service() -> Auth:
    raise NotImplementedError("Override this dependency with a concrete implementation")

def credentials(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Credentials:
    return Credentials(username=form.username, password=form.password)

@router.post('/token')
def get_token(credentials: Annotated[Credentials, Depends(credentials)], service: Annotated[Auth, Depends(service)]) -> Token:
    try:
        token = service.handle(credentials.username, credentials.password) 
        return Token(access_token=token.payload, token_type='Bearer')

    except Unauthorized:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
@router.post('/login', dependencies=[Security(bearer)])
def sign_in(request: Request):
    request.session['session'] = uuid4().hex
    return Response(status_code=status.HTTP_200_OK)

@router.post('/logout')
def sign_out(request: Request):
    try:
        request.session.pop('session')
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)