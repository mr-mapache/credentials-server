from typing import Annotated
from typing import Literal
from pydantic import BaseModel
from pydantic import Field
from pydantic import SecretStr
from pydantic import SecretBytes

class Schema(BaseModel):
    ...

class Credentials(BaseModel):
    username: Annotated[SecretStr, Field(...)]
    password: Annotated[SecretBytes, Field(...)]

class Token(BaseModel):
    access_token: Annotated[str, Field(...)]
    token_type: Annotated[Literal['Bearer', 'MAC'], Field(...)]