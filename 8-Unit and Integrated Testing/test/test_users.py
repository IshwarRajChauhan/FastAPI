from .utils import *
from routers.Users import get_db , get_current_user
from models import Todos
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user




def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'irc'
    assert response.json()['email'] == 'irc@email.com'
    assert response.json()['first_name'] == 'ir'
    assert response.json()['last_name'] == 'c'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == "0123456789"


