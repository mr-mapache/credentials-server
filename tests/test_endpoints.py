from fastapi.testclient import TestClient

def test_get_token_success(client: TestClient): 
    form_data = {"username":"johndoe", "password": "user@1234"}
    response = client.post("/token", data=form_data)
    assert response.status_code == 200
    json_data = response.json() 
    assert "access_token" in json_data
    assert json_data["token_type"] == "Bearer"