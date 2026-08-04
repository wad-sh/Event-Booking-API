from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy.orm import sessionmaker
from app.database.database import Base, get_db
from sqlalchemy import create_engine
from app.config import TEST_DATABASE_URL

test_engine = create_engine(TEST_DATABASE_URL)

test_session_local = sessionmaker(
    bind=test_engine,
    autoflush=False
)


@pytest.fixture
def db_session ():
    Base.metadata.create_all(bind=test_engine)

    db = test_session_local()

    yield db

    db.close()

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client (db_session):

    def override_get_db() :
            yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def reg_user (client) :
    user_data = {
        "username": "test_1",
        "email": "test1@gmail.com",
        "password": "123"
    }

    r = client.post(
        "/users/register",
        json=user_data
    )

    assert r.status_code == 200
    return user_data