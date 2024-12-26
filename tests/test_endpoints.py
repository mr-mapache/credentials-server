from fastapi import status
from fastapi.testclient import TestClient

def test_credentials(client: TestClient):
    response = client.post('/credentials/', json={'username':'test', 'password':'test'})
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post('/credentials/', json={'username':'test', 'password':'test'})
    assert response.status_code == status.HTTP_409_CONFLICT
    response = client.post('/credentials/verify', json={'username':'test', 'password':'test'})
    assert response.status_code == status.HTTP_200_OK
    response = client.post('/credentials/verify', json={'username':'test', 'password':'wrong'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED