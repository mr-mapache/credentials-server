from typing import Optional
from typing import Any  
from dataclasses import dataclass
from dataclasses import asdict 
from server.ports.claims import Subject

@dataclass
class Claims:
    iss: Optional[str] = None
    sub: Optional[str] = None
    aud: Optional[str] = None
    exp: Optional[int] = None
    nbf: Optional[int] = None
    iat: Optional[int] = None 

    def dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value}


class Authority:

    def sign(self, subject: Subject) -> Claims: 
        return Claims(iss=str(subject.id))