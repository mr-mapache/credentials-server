from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi import Response
from credentials.schemas import Credential
from credentials.ports import Credentials

router = APIRouter()

def credentials_port(*args, **kargs) -> Credentials:
    raise NotImplementedError("Override this port with a concrete implementation")

def security_port(credential: Credential) -> Credential:
    raise NotImplementedError("Override this port with a concrete implementation")

@router.post('/credentials/')
def add_credential(credential: Annotated[Credential, Depends(security_port)], credentials: Annotated[Credentials, Depends(credentials_port)]):
    if credentials.exists(credential):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    credentials.add(credential)
    return Response(status_code=status.HTTP_201_CREATED)

@router.post('/credentials/verify')
def verify_credential(credential: Annotated[Credential, Depends(security_port)], credentials: Annotated[Credentials, Depends(credentials_port)]):
    if not credentials.exists(credential):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not credentials.verify(credential):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return Response(status_code=status.HTTP_200_OK)