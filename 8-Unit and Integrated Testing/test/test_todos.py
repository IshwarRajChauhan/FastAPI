from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from routers.todos import get_db
from routers.auth import get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from models import Todos

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {
        "username": "irc",
        "id": 1,
        "user_role": "admin",
    }


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
    db = TestingSessionLocal()

    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)

    try:
        yield todo
    finally:
        db.delete(todo)
        db.commit()
        db.close()


def test_read_all_authenticated(test_todo):
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'complete': False,
        'title': 'Learn to code!',
        'description': 'Need to learn everyday!',
        'id': 1,
        'priority': 5,
        'owner_id': 1
    }]