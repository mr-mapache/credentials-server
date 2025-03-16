from jose.jwt import encode, decode
from typing import Optional
from typing import Any 
from datetime import datetime, UTC  
from datetime import timedelta
from dataclasses import dataclass
from dataclasses import asdict
from server.settings import Settings
from server.adapters.claims import Claims
from server.adapters.credentials import Secret

@dataclass
class Headers:
    alg: str = 'HS256'
    typ: str = 'JWT'
    cty: Optional[str] = None 
    
    def dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value}

@dataclass
class Token:
    payload: str
    expires_at: datetime

    def __str__(self) -> str:
        return self.payload


class Cryptography:
    def __init__(self, key: Secret):
        self.key = key

    def encode(self, claims: Claims, headers: Optional[Headers] = None) -> Token:
        expires_at = datetime.fromtimestamp(int(claims.exp), tz=UTC) if claims.exp else datetime.now(tz=UTC) + timedelta(minutes=15)
        headers = headers or Headers()
        encoded = encode(
            claims.dict(),
            self.key.get_secret_value(),
            headers.alg,
            headers.dict()
        )
        return Token(payload=encoded, expires_at=expires_at)    

    def decode(self, payload: str) -> Claims:
        decoded = decode(payload)
        return Claims(**decoded)

 
class Tokens:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.cryptography = Cryptography(key=settings.cryptography.key)

    def issue(self, claims: Claims) -> Token:
        return self.cryptography.encode(claims)