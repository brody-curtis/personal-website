"""
Data fetchers for each prediction market platform.

Each function returns a pandas DataFrame of open/active binary markets
with best bid/ask prices. This is a straight refactor of the original
Colab notebook logic -- no behavioral changes, just organized into a
module and given a couple of small safety fixes (missing imports).
"""

import json
import time

import pandas as pd
import requests


# ---------------------------------------------------------------------------
# Polymarket
# ---------------------------------------------------------------------------

def get_polymarket_data(verbose=True):
    """
    Fetch all active Polymarket binary markets using keyset pagination,
    including real ask prices pulled directly from Gamma's bestBid/bestAsk
    fields (no per-market CLOB calls needed).
    """

    url = "https://gamma-api.polymarket.com/events/keyset"

    all_events = []
    cursor = None

    if verbose:
        print("Fetching events from Polymarket...")

    while True:
        params = {"limit": 500, "closed": "false", "active": "true"}
        if cursor:
            params["after_cursor"] = cursor

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            events = data.get("events", [])
            cursor = data.get("next_cursor")
        else:
            events = data
            cursor = None

        if not events:
            break

        all_events.extend(events)
        if verbose:
            print(f"Retrieved {len(all_events)} events...")

        if not cursor:
            break

        time.sleep(0.1)

    if verbose:
        print(f"Finished downloading {len(all_events)} events.")

    market_data = []

    for event in all_events:
        for market in event.get("markets", []):

            # Parse outcomes safely
            try:
                raw_outcomes = market.get("outcomes", "[]")
                outcomes = (
                    json.loads(raw_outcomes)
                    if isinstance(raw_outcomes, str)
                    else raw_outcomes
                )
            except Exception:
                continue

            # Keep only binary markets (exactly 2 mutually exclusive outcomes).
            # This includes team-vs-team / player-vs-player markets
            # (e.g. "Cardinals" / "Yankees"), not just literal "Yes"/"No"
            # markets -- Polymarket structures both the same way under the
            # hood, just with different outcome labels.
            if len(outcomes) != 2:
                continue

            # outcomes, outcomePrices, and clobTokenIds are parallel arrays
            # aligned by position, so we reference them by index (0/1)
            # rather than by name.
            try:
                raw_prices = market.get("outcomePrices", '["0","0"]')
                prices = (
                    json.loads(raw_prices)
                    if isinstance(raw_prices, str)
                    else raw_prices
                )

                outcome_a_name, outcome_b_name = outcomes[0], outcomes[1]
                yes_prob = float(prices[0])
                no_prob = float(prices[1])
            except Exception:
                continue

            # Skip markets that are effectively resolved
            if not (0.0 < yes_prob < 1.0):
                continue

            volume = float(market.get("volume", 0) or 0)
            if volume < 500:
                continue

            # --- Real ask/bid prices, straight from Gamma, no extra calls ---
            # bestBid/bestAsk on the market object refer to outcome[0]
            # (literally "Yes" for Yes/No markets, or the first-listed team/
            # player for game markets, e.g. "Cardinals" above). Fall back to
            # midpoint prob if the fields are missing/null (thin or
            # newly-listed markets).
            yes_bid = market.get("bestBid")
            yes_ask = market.get("bestAsk")

            try:
                yes_bid = float(yes_bid) if yes_bid is not None else None
            except (TypeError, ValueError):
                yes_bid = None

            try:
                yes_ask = float(yes_ask) if yes_ask is not None else None
            except (TypeError, ValueError):
                yes_ask = None

            # Complementary book: best_bid(YES) = 1 - best_ask(NO), and
            # best_ask(YES) = 1 - best_bid(NO). Derive the NO side from YES.
            no_ask = (1.0 - yes_bid) if yes_bid is not None else None
            no_bid = (1.0 - yes_ask) if yes_ask is not None else None

            market_data.append({
                "Platform": "Polymarket",
                "Event Title": event.get("title"),
                "Market Name": market.get("question"),
                "Poly Yes Ask": yes_ask if yes_ask is not None else yes_prob,
                "Poly No Ask": no_ask if no_ask is not None else no_prob,
                "Poly Yes Bid": yes_bid,
                "Poly No Bid": no_bid,
                # What "Yes"/"No" above actually refer to. For a real
                # Yes/No market these will literally be "Yes"/"No". For a
                # game market they'll be e.g. "Cardinals"/"Yankees" -- so
                # "Poly Yes Ask" is the cost to bet on Cardinals here, NOT
                # a literal yes/no bet.
                "Poly Outcome A Name": outcome_a_name,
                "Poly Outcome B Name": outcome_b_name,
                "Volume": volume,
                "Market ID": market.get("id"),
                "Condition ID": market.get("conditionId"),
                "Event URL": f"https://polymarket.com/event/{event.get('slug')}",
                "Slug": market.get("slug"),
                "End Date": market.get("endDate"),
            })

    df = pd.DataFrame(market_data)
    if not df.empty:
        df = df.sort_values("Volume", ascending=False).reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Kalshi
# ---------------------------------------------------------------------------

KALSHI_BASE = "https://api.elections.kalshi.com/trade-api/v2"


def _get_with_retry(url, params, verbose=True):
    for attempt in range(5):
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 429:
            wait = 2 ** attempt
            if verbose:
                print(f"Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError("Kept getting rate limited after 5 retries")


def get_event_titles(verbose=True):
    """Build event_ticker -> readable title map (events endpoint excludes MVE by default)."""
    titles = {}
    cursor = None
    while True:
        params = {"limit": 200, "status": "open"}
        if cursor:
            params["cursor"] = cursor
        data = _get_with_retry(f"{KALSHI_BASE}/events", params, verbose)
        for e in data.get("events", []):
            titles[e.get("event_ticker")] = (
                e.get("title") or e.get("sub_title") or e.get("event_ticker")
            )
        if verbose:
            print(f"Events fetched so far: {len(titles)}")
        cursor = data.get("cursor")
        if not cursor:
            break
        time.sleep(0.2)
    return titles


def get_kalshi_data(target=None, min_volume=500, test_mode=False, verbose=True):
    event_titles = get_event_titles(verbose)

    market_data = []
    cursor = None
    page_size = 20 if test_mode else 200
    if test_mode and target is not None:
        target = min(target, 10)

    while True:
        params = {"limit": page_size, "status": "open", "mve_filter": "exclude"}
        if cursor:
            params["cursor"] = cursor
        data = _get_with_retry(f"{KALSHI_BASE}/markets", params, verbose)
        markets = data.get("markets", [])

        for m in markets:
            try:
                yes_bid = float(m.get("yes_bid_dollars", "0"))
                yes_ask = float(m.get("yes_ask_dollars", "0"))
            except (TypeError, ValueError):
                continue
            if yes_bid <= 0 or yes_ask <= 0:
                continue

            volume = float(m.get("volume_fp", 0) or 0)
            if volume <= min_volume:
                continue

            event_ticker = m.get("event_ticker")
            event_title = event_titles.get(event_ticker, event_ticker)
            leg = m.get("yes_sub_title") or m.get("title") or m.get("ticker")
            question = f"{event_title}: {leg}"

            market_data.append({
                "Platform": "Kalshi",
                "Ticker": m["ticker"],
                "Question": question,
                "Kalshi Yes Bid": yes_bid,
                "Kalshi Yes Ask": yes_ask,
                "Kalshi No Bid": float(m.get("no_bid_dollars", 0) or 0),
                "Kalshi No Ask": float(m.get("no_ask_dollars", 0) or 0),
                "Mid": (yes_bid + yes_ask) / 2,
                "Spread": yes_ask - yes_bid,
                "Kalshi Close Time": m.get("close_time"),
                "Volume": volume,
                "Open Interest": float(m.get("open_interest_fp", 0) or 0),
            })

        if verbose:
            print(f"Fetched page of {len(markets)} markets, running total: {len(market_data)} valid")
        if target is not None and len(market_data) >= target:
            break
        cursor = data.get("cursor")
        if not cursor:
            break
        time.sleep(0.3)

    return pd.DataFrame(market_data)


# ---------------------------------------------------------------------------
# PredictIt
# ---------------------------------------------------------------------------

def get_predictit_data(verbose=True):
    """Fetch all open PredictIt markets/contracts in a single call."""
    url = "https://www.predictit.org/api/marketdata/all/"

    if verbose:
        print("Fetching markets from PredictIt...")

    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()

    markets = data.get("markets", [])
    if verbose:
        print(f"Retrieved {len(markets)} markets.")

    market_data = []

    for market in markets:
        market_name = market.get("name")
        market_id = market.get("id")
        market_url = market.get("url")

        for contract in market.get("contracts", []):
            if contract.get("status") != "Open":
                continue

            yes_ask = contract.get("bestBuyYesCost")
            no_ask = contract.get("bestBuyNoCost")

            if yes_ask is None or no_ask is None:
                continue

            try:
                yes_ask = float(yes_ask)
                no_ask = float(no_ask)
            except (TypeError, ValueError):
                continue

            contract_name = contract.get("name") or contract.get("shortName")
            question = f"{market_name}: {contract_name}"

            market_data.append({
                "Platform": "PredictIt",
                "Market Name": question,
                "PredictIt Yes Ask": yes_ask,
                "PredictIt No Ask": no_ask,
                "PredictIt Yes Bid": contract.get("bestSellYesCost"),
                "PredictIt No Bid": contract.get("bestSellNoCost"),
                "Last Trade Price": contract.get("lastTradePrice"),
                "PredictIt End Date": contract.get("dateEnd"),
                "Contract ID": contract.get("id"),
                "Market ID": market_id,
                "Market URL": market_url,
            })

    return pd.DataFrame(market_data)
