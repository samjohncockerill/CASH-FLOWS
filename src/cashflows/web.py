"""Servidor web local para el analizador de flujos de caja.

Solo stdlib. Arranca con: `python -m cashflows.cli serve --port 8000`.
"""
from __future__ import annotations

import json
import mimetypes
import os
import threading
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

from . import core, loan as loan_mod

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


def _analyze(rate: float, flows: list[float]) -> dict:
    invested = -sum(cf for cf in flows if cf < 0)
    received = sum(cf for cf in flows if cf > 0)

    npv_val = core.npv(rate, flows)
    try:
        irr_val: Optional[float] = core.irr(flows)
    except Exception:
        irr_val = None
    try:
        mirr_val: Optional[float] = core.mirr(flows, rate, rate)
    except Exception:
        mirr_val = None
    pb = core.payback_period(flows)
    try:
        pi: Optional[float] = core.profitability_index(rate, flows)
    except Exception:
        pi = None

    cumulative, run = [], 0.0
    for cf in flows:
        run += cf
        cumulative.append(round(run, 6))

    decision = "INVERTIR" if (npv_val > 0 and (irr_val is None or irr_val > rate)) else "RECHAZAR"

    return {
        "rate": rate,
        "flows": flows,
        "invested": invested,
        "received": received,
        "net": received - invested,
        "cumulative": cumulative,
        "metrics": {
            "npv": npv_val,
            "irr": irr_val,
            "mirr": mirr_val,
            "payback": pb,
            "profitability_index": pi,
        },
        "decision": decision,
    }


def _loan(principal: float, rate: float, years: float, max_rows: int = 60) -> dict:
    s = loan_mod.amortize(principal, rate, years)
    schedule = [asdict(r) for r in s.schedule]
    if len(schedule) > max_rows:
        head = schedule[: max_rows // 2]
        tail = schedule[-max_rows // 2 :]
        sample = head + tail
    else:
        sample = schedule
    return {
        "principal": s.principal,
        "annual_rate": s.annual_rate,
        "months": s.months,
        "monthly_payment": s.monthly_payment,
        "total_paid": s.total_paid,
        "total_interest": s.total_interest,
        "schedule": schedule,
        "schedule_sample": sample,
    }


def _sensitivity(flows: list[float], r_from: float, r_to: float, step: float) -> dict:
    rates, r = [], r_from
    while r <= r_to + 1e-9:
        rates.append(round(r, 6))
        r += step
    points = [{"rate": rt, "npv": core.npv(rt, flows)} for rt in rates]
    try:
        irr_val: Optional[float] = core.irr(flows)
    except Exception:
        irr_val = None
    return {"points": points, "irr": irr_val}


def _read_static(path: str):
    safe = os.path.normpath(path).lstrip(os.sep).replace("..", "")
    full = os.path.join(STATIC_DIR, safe) if safe else os.path.join(STATIC_DIR, "index.html")
    if os.path.isdir(full):
        full = os.path.join(full, "index.html")
    if not full.startswith(STATIC_DIR) or not os.path.isfile(full):
        return None, None
    ctype, _ = mimetypes.guess_type(full)
    with open(full, "rb") as f:
        return f.read(), ctype or "application/octet-stream"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quieter logs
        return

    def _json(self, status: int, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw or b"{}")

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            data, ctype = _read_static("index.html")
        else:
            data, ctype = _read_static(path.lstrip("/"))
        if data is None:
            self.send_error(404, "Not Found")
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        try:
            payload = self._read_json()
            if self.path == "/api/analyze":
                rate = float(payload["rate"])
                flows = [float(x) for x in payload["flows"]]
                self._json(200, _analyze(rate, flows))
            elif self.path == "/api/loan":
                self._json(
                    200,
                    _loan(
                        float(payload["principal"]),
                        float(payload["rate"]),
                        float(payload["years"]),
                        int(payload.get("max_rows", 60)),
                    ),
                )
            elif self.path == "/api/sensitivity":
                flows = [float(x) for x in payload["flows"]]
                self._json(
                    200,
                    _sensitivity(
                        flows,
                        float(payload.get("from", 0.0)),
                        float(payload.get("to", 0.30)),
                        float(payload.get("step", 0.02)),
                    ),
                )
            else:
                self.send_error(404, "Not Found")
        except (ValueError, KeyError, RuntimeError) as e:
            self._json(400, {"error": str(e)})


def serve(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    httpd = ThreadingHTTPServer((host, port), Handler)
    return httpd


def serve_forever(host: str = "127.0.0.1", port: int = 8000) -> None:
    httpd = serve(host, port)
    url = f"http://{host}:{port}/"
    print(f"Cashflows web server escuchando en {url}  (Ctrl+C para parar)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
    finally:
        httpd.server_close()


def serve_in_thread(host: str = "127.0.0.1", port: int = 0):
    httpd = serve(host, port)
    th = threading.Thread(target=httpd.serve_forever, daemon=True)
    th.start()
    return httpd, th
