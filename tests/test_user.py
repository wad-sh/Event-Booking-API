
def test_reg (client) :
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



