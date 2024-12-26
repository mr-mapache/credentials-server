from typing import Annotated
from fastapi import Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from credentials.schemas import Credential

basic_scheme = HTTPBasic()

def basic_security_adapter(credential: Annotated[HTTPBasicCredentials, Security(basic_scheme)]):
    return Credential(username=credential.username, password=credential.password)