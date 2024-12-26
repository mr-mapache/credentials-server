from sqlalchemy import Table, Column, Integer, String, Boolean, LargeBinary, TIMESTAMP
from sqlalchemy import func, MetaData, ForeignKey, UUID

metadata = MetaData()

usernames = Table(
    'usernames',
    metadata,
    Column('pk', Integer, primary_key=True),
    Column('username', String(255), nullable=False, unique=True)
)

passwords = Table(
    'passwords',
    metadata,
    Column('pk', Integer, primary_key=True),
    Column('username_pk', Integer, ForeignKey('usernames.pk'), nullable=False),
    Column('password_hash', LargeBinary, nullable=False),
    Column('password_version', Integer, default=1),
    Column('password_is_active', Boolean, default=True),
    Column('password_created_at', TIMESTAMP(timezone=True), server_default=func.now()),
    Column('password_updated_at', TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
)