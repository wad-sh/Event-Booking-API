def test_event_create_success (client,admin_token) :

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


def test_event_create_not_admin (client,user_token) :

    resp = client.post(
        "/events",
        headers={
            "Authorization" : f"Bearer {user_token}"
        },
        json={
            "title": "Python Conference",
            "description": "Backend event",
            "capacity": 100,
            "date": "2027-09-01T10:00:00+00:00"
        }
    )

    assert resp.status_code == 403
    assert resp.json()["detail"] == "you are not an admin"

def test_event_create_capacity_wrong (client,admin_token) :
    resp = client.post(
            "/events",
            headers={
                "Authorization" : f"Bearer {admin_token}"
            },
            json={
                "title": "Python Conference",
                "description": "Backend event",
                "capacity": 0,
                "date": "2027-09-01T10:00:00+00:00"
            }
        )
    
    assert resp.status_code == 400
    assert resp.json()["detail"] == "capacity should be more than 0"

    

def test_event_create_date_wrong (client,admin_token) :
    resp = client.post(
            "/events",
            headers={
                "Authorization" : f"Bearer {admin_token}"
            },
            json={
                "title": "Python Conference",
                "description": "Backend event",
                "capacity": 100,
                "date": "2024-09-01T10:00:00+00:00"
            }
        )
    
    assert resp.status_code == 400
    assert resp.json()["detail"] == "event date must be in the future"


def test_event_create_no_token (client) :

    resp = client.post(
        "/events",
        json={
            "title": "Python Conference",
            "description": "Backend event",
            "capacity": 100,
            "date": "2027-09-01T10:00:00+00:00"
        }
    )
    assert resp.status_code == 401


def test_get_all_events (client) :
    r = client.get(
        "/events"
    )
    assert r.status_code == 200
    assert r.json() == []

def test_get_event_success (client,event) :
    r = client.get(
            f"/events/{event}"
        )
    assert r.status_code == 200
    assert r.json()["id"] == event

def test_get_event_fail (client) :
    r = client.get(
        "/events/100"
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "can't find event"

def test_update_event_description_success (client,admin_token,event) :
    r = client.put(
        f"/events/{event}",
        headers={
            "Authorization" : f"Bearer {admin_token}"
        },
        json={
            "description" : "Something"
        }
    )
    assert r.status_code == 200
    assert r.json()["description"] == "Something"

def test_update_event_capacity_success(client, admin_token, event):
    r = client.put(
        f"/events/{event}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "capacity": 200
        }
    )

    assert r.status_code == 200
    assert r.json()["capacity"] == 200

def test_update_event_date_success(client, admin_token, event):
    r = client.put(
        f"/events/{event}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "date": "2028-09-01T10:00:00+00:00"
        }
    )

    assert r.status_code == 200
    assert r.json()["date"].startswith("2028")

def test_update_event_not_admin (client,user_token,event) :
    r = client.put(
        f"/events/{event}",
        headers={
            "Authorization" : f"Bearer {user_token}"
        },
        json={
            "description" : "Changed"
        }
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "you are not an admin"

def test_update_event_no_token (client,event) :
    r = client.put(
        f"/events/{event}",
        json={
            "description" : "Changed"
        }
    )
    assert r.status_code == 401


def test_update_event_no_change (client,admin_token,event) :
    r = client.put(
        f"/events/{event}",
        headers={
            "Authorization" : f"Bearer {admin_token}"
        },
        json={}
        )
    assert r.status_code == 400
    assert r.json()["detail"] == "no change"

def test_update_event_not_found (client,admin_token) :
    r = client.put(
            f"/events/100",
            headers={
                "Authorization" : f"Bearer {admin_token}"
            },
            json={
                "description" : "Something"
            }
        )
    assert r.status_code == 404
    assert r.json()["detail"] == "can't find event"

def test_update_event_wrong_capacity (client,admin_token,event) :
    r = client.put(
        f"/events/{event}",
        headers={
            "Authorization" : f"Bearer {admin_token}"
        },
        json={
            "capacity" :0
        }
        )
    assert r.status_code == 400
    assert r.json()["detail"] == "positive numbers only from capacity"

def test_update_event_wrong_date (client,admin_token,event) :
    r = client.put(
        f"/events/{event}",
        headers={
            "Authorization" : f"Bearer {admin_token}"
        },
        json={
            "date" : "2023-09-01T10:00:00+00:00"
        }
        )
    assert r.status_code == 400
    assert r.json()["detail"] == "event date must be in the future"

def test_delete_event_success (client,admin_token,event) :
    r =client.delete(
        f"/events/{event}",
        headers={
            "Authorization" : f"Bearer {admin_token}"
        }
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Event deleted"

    check = client.get(f"/events/{event}")
    assert check.status_code == 404

def test_delete_event_not_admin (client,user_token,event) :
    r =client.delete(
        f"/events/{event}",
        headers={
            "Authorization" : f"Bearer {user_token}"
        }
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "you are not an admin"

def test_delete_event_no_token(client,event) :
    r =client.delete(
            f"/events/{event}"
        )
    assert r.status_code == 401


def test_delete_event_not_found (client,admin_token) :
    r =client.delete(
        f"/events/100",
        headers={
            "Authorization" : f"Bearer {admin_token}"
        }
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "can't find event"
