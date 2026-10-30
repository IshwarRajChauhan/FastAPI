from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from database import Base
from main import app
from routers.todos import get_db
from routers.auth import get_current_user,bcrypt_context
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from models import Todos,users


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

    db.query(Todos).delete()
    db.commit()

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
        db.query(Todos).delete()
        db.commit()
        db.close()





@pytest.fixture
def test_user():
    user = users(
        username="irc",
        email="irc@email.com",
        first_name="ir",
        last_name="c",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="0123456789"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()






