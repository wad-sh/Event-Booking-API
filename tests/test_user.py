
def test_register_success (client) :
    response = client.post(
        "/users/register",
        json={
            "username" : "test_1",
            "email" : "test1@gmail.com",
            "password" : "123"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == "test_1"
    assert response.json()["email"] == "test1@gmail.com"



def test_reg_used_username (client,user) :
    
    response = client.post(
        "/users/register",
        json={
                    "username" : "test_1",
                    "email" : "t111122@gmail.com",
                    "password" : "123"
                }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "username already existed"

def test_reg_used_email (client,user) :
    

    response = client.post(
        "/users/register",
        json={
                    "username" : "test1111",
                    "email" : "test1@gmail.com",
                    "password" : "123"
                }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "email already existed"


def test_login_success (client,user) :
    

    response = client.post(
        "/users/login",
        data={
            "username" : "test1@gmail.com",
            "password" : "123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password (client,user) :
    

    response = client.post(
            "/users/login",
            data={
                "username" : "test1@gmail.com",
                "password" : "4444"
            }
        )

    assert response.status_code == 401
    assert response.json()["detail"] =="wrong email or password"

def test_login_wrong_email (client,user) :
    
    
    response = client.post(
                "/users/login",
                data={
                    "username" : "test10000@gmail.com",
                    "password" : "123"
                }
            )
    
    assert response.status_code == 401
    assert response.json()["detail"] =="wrong email or password"
    
    