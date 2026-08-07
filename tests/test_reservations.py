def test_reservation_success_as_a_user (client,user_token,event) :
    r = client.post(
        f"/events/{event}/reserve",
        headers={
            "Authorization" : f"Bearer {user_token}"
        }
    )

    assert r.status_code == 200
    assert "id" in r.json()

def test_reservation_success_as_an_admin (client,admin_token,event) :
    r = client.post(
        f"/events/{event}/reserve",
        headers={
            "Authorization" : f"Bearer {admin_token}"
        }
    )

    assert r.status_code == 200
    assert "id" in r.json()

def test_reservation_no_token (client,event) :
    r = client.post(
        f"/events/{event}/reserve",
    )

    assert r.status_code == 401

def test_reservation_event_not_found (client,user_token) :
    r = client.post(
            f"/events/1000/reserve",
            headers={
                "Authorization" : f"Bearer {user_token}"
            }
        )
    
    assert r.status_code == 404
    assert r.json()["detail"] == "no event has been found"


def test_reservation_already_exists (client,user_token,event,reservation) :

    r = client.post(
            f"/events/{event}/reserve",
            headers={
                "Authorization" : f"Bearer {user_token}"
            }
        )
    
    assert r.status_code == 409
    assert r.json()["detail"] == "Reservation already existed"


def test_reservation_full_event (client,user_token,full_event) :
    r = client.post(
            f"/events/{full_event}/reserve",
            headers={
                "Authorization" : f"Bearer {user_token}"
            }
        )
    
    assert r.status_code == 409
    assert r.json()["detail"] == "no room left"



def test_reservation_delete_success (client,user_token,event,reservation) :
    r = client.delete(
                f"/events/{event}/reserve",
                headers={
                    "Authorization" : f"Bearer {user_token}"
                }
            )
    assert r.status_code == 200
    assert r.json()["message"] == "Reservation deleted"


def test_reservation_delete_no_reservation (client,user_token,event) :
    r = client.delete(
                f"/events/{event}/reserve",
                headers={
                    "Authorization" : f"Bearer {user_token}"
                }
            )
    assert r.status_code == 404
    assert r.json()["detail"] == "Reservation or event not found"


def test_reservation_delete_no_event (client,user_token,reservation) :
    r = client.delete(
                f"/events/10000/reserve",
                headers={
                    "Authorization" : f"Bearer {user_token}"
                }
            )
    assert r.status_code == 404
    assert r.json()["detail"] == "Reservation or event not found"

def test_reservation_delete_no_token (client,event,reservation) :
    r = client.delete(
                f"/events/{event}/reserve"
            )
    assert r.status_code == 401
