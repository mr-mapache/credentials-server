from typing import override

from sqlalchemy.orm import Session
from sqlalchemy.sql import insert, select

from credentials.ports import Credentials as Collection
from credentials.ports import Cryptography
from credentials.schemas import Credential
from credentials.adapters.schemas import usernames, passwords

class Credentials(Collection):
    def __init__(self, session: Session, cryptography: Cryptography):
        self.session = session
        self.cryptography = cryptography

    @override
    def add(self, credential: Credential) -> None:
        command = (
            insert(usernames).
            values(username=credential.username.get_secret_value()).
            returning(usernames.columns.pk)
        )
        result = self.session.execute(command)
        username_pk = result.scalars().one()
        command = (
            insert(passwords).
            values(username_pk=username_pk, password_hash=self.cryptography.hash(credential.password))
        )
        self.session.execute(command)

    @override
    def exists(self, credential: Credential) -> bool:
        query = (
            select(usernames).
            where(usernames.columns.username == credential.username.get_secret_value())
        )
        result = self.session.execute(query)
        return True if result.scalars().first() else False

    @override
    def verify(self, credential: Credential) -> bool:
        query = (
            select(passwords).
            join(usernames, usernames.columns.pk == passwords.columns.username_pk).
            where(usernames.columns.username == credential.username.get_secret_value()).
            order_by(passwords.columns.password_created_at.desc()).
            limit(1)
        )
        result = self.session.execute(query)
        row = result.fetchone()
        if not row or not row.password_is_active:
            return False
        return self.cryptography.verify(credential.password, row.password_hash)