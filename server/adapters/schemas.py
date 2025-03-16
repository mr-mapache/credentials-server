from uuid import UUID
from typing import Any
from datetime import datetime 
from dataclasses import dataclass
from sqlalchemy import TIMESTAMP
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from server.ports.users import Credentials 

@dataclass
class Owner:
    id: Any

class Schema(DeclarativeBase):
    pk: Mapped[int] = mapped_column(primary_key=True)

class User(Schema):
    __tablename__ = 'users'
    __allow_unmapped__ = True
    id: Mapped[UUID] = mapped_column('user_id', unique=True, nullable=False)   
    username: Mapped[str] = mapped_column('user_username', unique=True, nullable=True)
    credentials: Credentials = None

class Password(Schema):
    __tablename__ = 'passwords'
    pk: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    hash: Mapped[bytes] = mapped_column('password_hash', nullable=False)
    version: Mapped[int] = mapped_column('password_version', default=1)
    is_active: Mapped[bool] = mapped_column('password_is_active', default=True)
    created_at: Mapped[datetime] = mapped_column('password_created_at', TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column('password_updated_at', TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    user_pk: Mapped[int] = mapped_column(ForeignKey('users.pk', ondelete='CASCADE'), nullable=False)