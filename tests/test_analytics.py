def _add(client, headers, company, source, status):
    r = client.post(
        "/applications",
        json={"company": company, "role": "SDE", "source": source, "status": status},
        headers=headers,
    )
    assert r.status_code == 201


def test_summary_rates(client, auth_headers):
    _add(client, auth_headers, "A", "linkedin", "applied")
    _add(client, auth_headers, "B", "linkedin", "interview")
    _add(client, auth_headers, "C", "referral", "offer")
    _add(client, auth_headers, "D", "portal", "rejected")

    s = client.get("/analytics/summary", headers=auth_headers).json()
    assert s["total"] == 4
    assert s["by_status"]["applied"] == 1
    assert s["response_rate_pct"] == 75.0   # 3 of 4 got any response
    assert s["interview_rate_pct"] == 50.0  # interview + offer
    assert s["offer_rate_pct"] == 25.0


def test_summary_empty(client, auth_headers):
    s = client.get("/analytics/summary", headers=auth_headers).json()
    assert s["total"] == 0
    assert s["response_rate_pct"] == 0.0


def test_by_source(client, auth_headers):
    _add(client, auth_headers, "A", "referral", "interview")
    _add(client, auth_headers, "B", "portal", "applied")
    _add(client, auth_headers, "C", "portal", "applied")

    rows = {r["source"]: r for r in client.get("/analytics/by-source", headers=auth_headers).json()}
    assert rows["referral"]["response_rate_pct"] == 100.0
    assert rows["portal"]["total"] == 2
    assert rows["portal"]["response_rate_pct"] == 0.0


def test_analytics_scoped_to_user(client, auth_headers, other_headers):
    _add(client, auth_headers, "A", "linkedin", "offer")
    s = client.get("/analytics/summary", headers=other_headers).json()
    assert s["total"] == 0
