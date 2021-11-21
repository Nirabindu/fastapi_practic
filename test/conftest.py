from fastapi.testclient import TestClient
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app    

@pytest.fixture
def client():
    client = TestClient(app)
    yield client

@pytest.fixture
def token_header(client:TestClient):
    username = "bnxxc809@gmail.com"
    password = "123"
    data = {'username':username,'password':password}
    response = client.post('/user_login',data = data)
    access_token = response.json()['access_token']
    
    return{'Authorization':f'Bearer {access_token}'}
