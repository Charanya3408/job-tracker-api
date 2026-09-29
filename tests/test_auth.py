def test_register_success(client):
    r = client.post(
        "/auth/register", json={"email": "new@example.com", "password": "testpass123"}
    )
    assert r.status_code == 201
    assert r.json()["email"] == "new@example.com"
    assert "password" not in r.json()
    assert "hashed_password" not in r.json()


def test_register_duplicate_email(client):
    body = {"email": "dup@example.com", "password": "testpass123"}
    client.post("/auth/register", json=body)
    r = client.post("/auth/register", json=body)
    assert r.status_code == 409


def test_register_short_password_rejected(client):
    r = client.post(
        "/auth/register", json={"email": "x@example.com", "password": "short"}
    )
    assert r.status_code == 422


def test_login_wrong_password(client):
    client.post(
        "/auth/register", json={"email": "u@example.com", "password": "testpass123"}
    )
    r = client.post(
        "/auth/login", data={"username": "u@example.com", "password": "wrongpass1"}
    )
    assert r.status_code == 401


def test_me_requires_token(client):
    assert client.get("/auth/me").status_code == 401


def test_me_returns_current_user(client, auth_headers):
    r = client.get("/auth/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["email"] == "a@example.com"
