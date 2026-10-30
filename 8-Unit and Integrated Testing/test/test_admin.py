from .utils import *
from routers.admin import get_db , get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [{
        'description': 'Need to learn everyday!',
        'title': 'Learn to code!',
        'complete': False,
        'priority': 5,
        'id': 1,
        'owner_id': 1
    }]









