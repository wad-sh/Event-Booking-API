from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy.orm import sessionmaker
from app.database.database import Base, get_db
from sqlalchemy import create_engine
from app.config import TEST_DATABASE_URL
from app.models.user import User
from app.auth.security import hash_pw
from app.enums.adminuser import AdminUser


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
def user (client) :
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

@pytest.fixture
def admin_user (db_session) :
    admin = User(
         username = "admin1",
         email = "admin@gmail.com",
         hashed_password = hash_pw("123"),
         role=AdminUser.admin
                 )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh (admin)

    return admin

@pytest.fixture
def admin_token (client,admin_user) :
    login_resp = client.post(
         "/users/login",
         data={
              "username" : admin_user.email,
              "password" : "123"
         }
    
    )
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()

    return login_resp.json()["access_token"]

@pytest.fixture
def user_token (client,user) :
    login_resp = client.post(
         "/users/login",
         data={
              "username": user["email"],
              "password" : "123"
         }
    
    )
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()

    return login_resp.json()["access_token"]

@pytest.fixture
def event (client,admin_token) :
    resp = client.post(
            "/events",
            headers={
                "Authorization" : f"Bearer {admin_token}"
            },
            json={
                "title": "Python Conference",
                "description": "Backend event",
                "capacity": 100,
                "date": "2027-09-01T10:00:00+00:00"
            }
        )
    
    assert resp.status_code == 201
    assert resp.json()["title"] == "Python Conference"

    return int(resp.json()["id"])
@pytest.fixture
def full_event (client,admin_token) :
    resp = client.post(
            "/events",
            headers={
                "Authorization" : f"Bearer {admin_token}"
            },
            json={
                "title": "Project",
                "description": "",
                "capacity": 1,
                "date": "2027-07-01T10:00:00+00:00"
            }
        )
    
    assert resp.status_code == 201
    assert resp.json()["title"] == "Project"

    e_id = int(resp.json()["id"])

    reserv = client.post(
        f"/events/{e_id}/reserve",
        headers={
                        "Authorization" : f"Bearer {admin_token}"
                }
    )
    assert reserv.status_code == 200
    return e_id

@pytest.fixture
def reservation (client,event,user_token) :
    r = client.post(
            f"/events/{event}/reserve",
            headers={
                "Authorization" : f"Bearer {user_token}"
            }
        )
    
    assert r.status_code == 200
    assert "id" in r.json()
