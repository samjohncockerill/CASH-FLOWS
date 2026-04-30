import json
import urllib.request

import pytest

from cashflows.web import serve_in_thread


@pytest.fixture(scope="module")
def server():
    httpd, _ = serve_in_thread("127.0.0.1", 0)
    port = httpd.server_address[1]
    yield f"http://127.0.0.1:{port}"
    httpd.shutdown()
    httpd.server_close()


def _post(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as r:
        return r.status, json.loads(r.read())


def test_index_served(server):
    with urllib.request.urlopen(server + "/", timeout=5) as r:
        body = r.read().decode("utf-8")
    assert r.status == 200
    assert "Cash Flow Analyzer" in body


def test_api_analyze(server):
    status, data = _post(server + "/api/analyze", {"rate": 0.10, "flows": [-1000, 400, 400, 400]})
    assert status == 200
    assert "metrics" in data
    assert data["metrics"]["npv"] == pytest.approx(-5.2592, abs=1e-3)
    assert data["decision"] in ("INVERTIR", "RECHAZAR")


def test_api_loan(server):
    status, data = _post(server + "/api/loan", {"principal": 200000, "rate": 0.045, "years": 30})
    assert status == 200
    assert data["months"] == 360
    assert data["monthly_payment"] == pytest.approx(1013.37, abs=0.5)
    assert len(data["schedule"]) == 360


def test_api_sensitivity(server):
    status, data = _post(
        server + "/api/sensitivity",
        {"flows": [-1000, 400, 400, 400], "from": 0, "to": 0.20, "step": 0.05},
    )
    assert status == 200
    assert len(data["points"]) == 5
    assert data["points"][0]["rate"] == 0.0
    assert data["points"][0]["npv"] == pytest.approx(200.0)


def test_api_bad_input(server):
    req = urllib.request.Request(
        server + "/api/analyze",
        data=b'{"rate": "not-a-number", "flows": [1,2]}',
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=5)
        raised = False
    except urllib.error.HTTPError as e:
        raised = True
        assert e.code == 400
    assert raised
