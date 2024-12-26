from typing import override
from passlib.context import CryptContext
from credentials.schemas import SecretBytes
from credentials.ports import Cryptography as Service
from credentials.settings import Settings

class Cryptography(Service):
    def __init__(self, settings: Settings):
        self.context = CryptContext(schemes=settings.cryptography.schemes)
    
    @override
    def hash(self, password: SecretBytes) -> bytes:
        return self.context.hash(password.get_secret_value()).encode('utf-8')
    
    @override
    def verify(self, password: SecretBytes, hash: bytes) -> bool:
        return self.context.verify(password.get_secret_value(), hash)