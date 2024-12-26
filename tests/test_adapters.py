from credentials.schemas import SecretBytes
from credentials.schemas import Credential
from credentials.ports import Cryptography
from credentials.ports import Credentials

def test_cryptography(cryptography: Cryptography):
    password = SecretBytes('test')
    wrong = SecretBytes('wrong')
    hash = cryptography.hash(password)
    assert cryptography.verify(password, hash)
    assert not cryptography.verify(wrong, hash)

def test_credentials(credentials: Credentials):
    credentials.add(Credential(username='test', password='test'))
    assert credentials.exists(Credential(username='test', password='test'))
    assert not credentials.exists(Credential(username='none', password='test'))

    assert credentials.verify(Credential(username='test', password='test'))
    assert not credentials.verify(Credential(username='test', password='wrong'))
    assert not credentials.verify(Credential(username='none', password='test'))