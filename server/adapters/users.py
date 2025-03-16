from uuid import UUID, uuid4 
from typing import Optional  
from sqlalchemy.sql import insert, update, select, delete
from sqlalchemy.orm import Session
from server.settings import Settings
from server.connections import Connections
from server.adapters.schemas import User, Owner  
from server.adapters.credentials import Credentials, reveal, Secret

class Users:
    def __init__(self, connections: Connections, settings: Settings):
        self.connections = connections
        self.settings = settings

    @property
    def sql(self) -> Session:
        return self.connections.sql

    def create(self, id: UUID) -> User: 
        command = insert(User).values(id=id).returning(User.pk)
        result = self.sql.execute(command)
        user_pk = result.scalar()
        user = User(pk=user_pk, id=id) 
        user.credentials = Credentials(self.connections, self.settings, Owner(id=user.pk)) 
        return user
    
    def get(self, id: UUID) -> Optional[User]:
        query = select(User).where(User.id == id)
        result = self.sql.execute(query)
        user = result.scalars().first()
        if user:
            user.credentials = Credentials(self.connections, self.settings, Owner(id=user.pk)) 
            return user
        else:
            return None

    def read(self, by: str, **kwargs) -> Optional[User]: 
        user = None
        
        match by:
            case 'credentials':
                query = select(User).where(User.username == reveal(kwargs['username']))
                result = self.sql.execute(query)
                user = result.scalars().first()
            case _:
                raise KeyError("Invalid query key")

        if user:
            user.credentials = Credentials(self.connections, self.settings, Owner(id=user.pk)) 
            return user
        else:
            return None
        
    def update(self, id: UUID, username: Secret): 
        command = update(User).values(value=username).where(User.id == id)
        self.sql.execute(command)
    
    def delete(self, id: UUID) -> None:
        command = delete(User).where(User.id == id)
        self.sql.execute(command)