JOB = {"company": "Zoho", "role": "Software Developer", "source": "linkedin"}


def test_create_and_list(client, auth_headers):
    r = client.post("/applications", json=JOB, headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["status"] == "applied"

    listed = client.get("/applications", headers=auth_headers).json()
    assert len(listed) == 1
    assert listed[0]["company"] == "Zoho"


def test_requires_auth(client):
    assert client.get("/applications").status_code == 401
    assert client.post("/applications", json=JOB).status_code == 401


def test_cannot_access_another_users_application(client, auth_headers, other_headers):
    app_id = client.post("/applications", json=JOB, headers=auth_headers).json()["id"]

    assert client.get(f"/applications/{app_id}", headers=other_headers).status_code == 404
    assert (
        client.patch(
            f"/applications/{app_id}", json={"status": "offer"}, headers=other_headers
        ).status_code
        == 404
    )
    assert client.delete(f"/applications/{app_id}", headers=other_headers).status_code == 404
    assert client.get("/applications", headers=other_headers).json() == []


def test_update_status(client, auth_headers):
    app_id = client.post("/applications", json=JOB, headers=auth_headers).json()["id"]
    r = client.patch(
        f"/applications/{app_id}", json={"status": "interview"}, headers=auth_headers
    )
    assert r.status_code == 200
    assert r.json()["status"] == "interview"
    assert r.json()["company"] == "Zoho"  # untouched fields preserved


def test_filter_by_status(client, auth_headers):
    client.post("/applications", json=JOB, headers=auth_headers)
    client.post(
        "/applications",
        json={**JOB, "company": "Freshworks", "status": "offer"},
        headers=auth_headers,
    )
    r = client.get("/applications?status=offer", headers=auth_headers)
    assert [a["company"] for a in r.json()] == ["Freshworks"]


def test_delete(client, auth_headers):
    app_id = client.post("/applications", json=JOB, headers=auth_headers).json()["id"]
    assert client.delete(f"/applications/{app_id}", headers=auth_headers).status_code == 204
    assert client.get(f"/applications/{app_id}", headers=auth_headers).status_code == 404
