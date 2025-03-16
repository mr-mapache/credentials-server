from typing import Protocol

from bcrypt import checkpw, hashpw, gensalt 
from sqlalchemy.sql import insert, select, update
from sqlalchemy.orm import Session

from server.settings import Settings
from server.connections import Connections
from server.adapters.schemas import User, Password, Owner

class Secret(Protocol):

    def get_secret_value() -> str | bytes:
        ...

def reveal(secret: Secret) -> str | bytes:
    return secret.get_secret_value()


class Cryptography:
    def __init__(self, settings: Settings):
        self.settings = settings

    def verify(self, secret: Secret, hash: bytes) -> bool:
        return checkpw(reveal(secret), hash)

    def hash(self, secret: Secret) -> bytes:
        return hashpw(reveal(secret), gensalt())
    

class Credentials:
    def __init__(self, connections: Connections, settings: Settings, owner: Owner):
        self.connections = connections 
        self.owner = owner
        self.cryptography = Cryptography(settings)

    @property
    def sql(self) -> Session:
        return self.connections.sql
    
    def add(self, username: Secret, password: Secret) -> None:
        command = update(User).values(username=reveal(username)).returning(User.pk)
        result = self.sql.execute(command)
        user_pk = result.scalar()
        hash = self.cryptography.hash(password)
        command = insert(Password).values(hash=hash, user_pk=user_pk)
        self.sql.execute(command)

    def verify(self, username: Secret, password: Secret) -> bool:
        query = select(Password).join(User).where(User.username == reveal(username)).order_by(Password.created_at.desc()).limit(1)
        result = self.sql.execute(query)
        secret = result.scalars().first()
        if not secret:
            return False 
        verified = self.cryptography.verify(password, secret.hash)
        return True if verified else False