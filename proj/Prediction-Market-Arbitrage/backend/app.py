"""
Local Flask app: serves the frontend and exposes /api/arbs, which runs
a fresh scan across Polymarket, Kalshi and PredictIt every time it's
called (that's what the frontend's Refresh button hits).

Run with:
    pip install -r requirements.txt
    python backend/app.py

Then open http://127.0.0.1:5000
"""

import os
import threading
import traceback
from datetime import datetime, timezone

from flask import Flask, jsonify, send_from_directory

from scraper import get_polymarket_data, get_kalshi_data, get_predictit_data
from matcher import run_arbitrage_scan

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

# Simple in-memory cache so a page load doesn't have to wait on a scan;
# the Refresh button calls /api/arbs?force=1 to bypass it.
_lock = threading.Lock()
_cache = {"data": [], "last_run": None, "error": None}

MIN_ROI_PCT = 2.0


def _run_scan():
    poly_df = get_polymarket_data()
    kalshi_df = get_kalshi_data()
    predictit_df = get_predictit_data()
    return run_arbitrage_scan(poly_df, kalshi_df, predictit_df, min_roi_pct=MIN_ROI_PCT)


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/api/arbs")
def api_arbs():
    with _lock:
        try:
            data = _run_scan()
            _cache["data"] = data
            _cache["last_run"] = datetime.now(timezone.utc).isoformat()
            _cache["error"] = None
        except Exception as exc:  # noqa: BLE001
            traceback.print_exc()
            _cache["error"] = str(exc)
            # keep serving the last good data if we have it

        return jsonify({
            "opportunities": _cache["data"],
            "last_run": _cache["last_run"],
            "error": _cache["error"],
        })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
