from uuid import uuid4
from server.ports.users import Users
from server.schemas import SecretStr, SecretBytes

def test_users(users: Users):
    id = uuid4()
    user = users.create(id=id)
    assert user.id == id
    user = users.get(id)
    assert user.id == id
    users.delete(id)
    user = users.get(id)
    assert not user

def test_credentials(users: Users):
    id = uuid4()
    user = users.create(id=id)
    user.credentials.add(SecretStr('test'), SecretBytes(b'test'))
    user = users.read(by='credentials', username=SecretStr('test'))
    assert user.id == id
    assert user.credentials.verify(SecretStr('test'), SecretBytes(b'test'))