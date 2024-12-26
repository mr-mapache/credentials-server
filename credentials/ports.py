from abc import ABC, abstractmethod
from credentials.schemas import SecretBytes
from credentials.schemas import Credential

class Cryptography(ABC):
    
    @abstractmethod
    def verify(self, password: SecretBytes, hash: bytes) -> bool:...

    @abstractmethod
    def hash(self, password: SecretBytes) -> bytes:...


class Credentials(ABC):
    cryptography: Cryptography

    @abstractmethod
    def add(self, credential: Credential) -> None:...

    @abstractmethod
    def exists(self, credential: Credential) -> bool:...

    @abstractmethod
    def verify(self, credential: Credential) -> bool:...