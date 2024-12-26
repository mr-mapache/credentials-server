from pydantic import BaseModel
from pydantic import SecretStr, SecretBytes

class Schema(BaseModel): ...

class Credential(Schema):
    username: SecretStr
    password: SecretBytes