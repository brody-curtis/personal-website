"""
Cross-platform market matching + arbitrage calculation.

Refactor of the original notebook's matching logic. The one addition
is explicit outcome labeling: every returned opportunity now says which
named outcome (e.g. "Portugal", "J.D. Vance") each leg's Yes/No price
refers to, rather than a bare "Yes"/"No" that only makes sense in the
context of one platform's phrasing.
"""

import re

import pandas as pd

# polyfuzz.metrics imports matplotlib.cm.get_cmap at load time (for a
# plotting helper we never call), but matplotlib 3.9+ removed that
# function in favor of matplotlib.colormaps[...]. Rather than pin an old
# matplotlib (which has no prebuilt wheel for newer Python on Windows,
# forcing a from-source build that needs MSVC build tools), patch the
# name back in before polyfuzz imports it. This works with whatever
# matplotlib pip installs normally.
import matplotlib.cm as _mpl_cm
if not hasattr(_mpl_cm, "get_cmap"):
    import matplotlib as _mpl

    def _get_cmap_shim(name=None, lut=None):
        return _mpl.colormaps[name] if name is not None else _mpl.colormaps["viridis"]

    _mpl_cm.get_cmap = _get_cmap_shim

from polyfuzz import PolyFuzz

# =============================================================================
# Shared filters (unchanged from the original notebook)
# =============================================================================

CONFLICT_PAIRS = [
    ("run", "win"), ("top", "win"), ("win", "lose"), ("tie", "win"),
    ("tie", "lose"), ("ballot", "win"), ("ballot", "lose"),
    ("above", "below"), ("over", "under"), ("before", "after"),
    ("increase", "decrease"), ("pass", "fail"), ("resign", "reelect"),
    ("nominate", "confirm"), ("2026", "2027"), ("2026", "2028"),
    ("2027", "2028"), ("win", "2nd"), ("win", "second"), ("win", "3rd"),
    ("win", "third"), ("1st", "2nd"), ("1st", "second"), ("1st", "3rd"),
    ("1st", "third"), ("2nd", "3rd"), ("2nd", "third"),
    ("de facto", "leader"), ("above", "be"), ("below", "be"),
]

REQUIRED_MATCH_WORDS = [
    "before", "after", "above", "below", "over", "under", "increase",
    "decrease", "2026", "2027", "2028", "least", "most", "win", "vice",
]


def has_required_word_mismatch(text_a, text_b, words=REQUIRED_MATCH_WORDS):
    a, b = text_a.lower(), text_b.lower()
    for word in words:
        has_a = re.search(rf'\b{re.escape(word)}\b', a) is not None
        has_b = re.search(rf'\b{re.escape(word)}\b', b) is not None
        if has_a != has_b:
            return True
    return False


def has_conflict(text_a, text_b, pairs=CONFLICT_PAIRS):
    a, b = text_a.lower(), text_b.lower()
    for w1, w2 in pairs:
        a1, a2 = re.search(rf'\b{w1}\b', a), re.search(rf'\b{w2}\b', a)
        b1, b2 = re.search(rf'\b{w1}\b', b), re.search(rf'\b{w2}\b', b)
        if (a1 and not a2 and b2 and not b1) or (a2 and not a1 and b1 and not b2):
            return True
    return False


CATEGORY_GROUPS = [
    {"over", "under", "o/u", "total"},
    {"spread", "handicap", "line", "margin"},
]


def _contains(text, term):
    if any(ch in term for ch in "/."):
        return term in text
    return re.search(rf'\b{re.escape(term)}\b', text) is not None


def category_mismatch(text_a, text_b, groups=CATEGORY_GROUPS):
    a, b = text_a.lower(), text_b.lower()
    for group in groups:
        a_has = any(_contains(a, t) for t in group)
        b_has = any(_contains(b, t) for t in group)
        if a_has != b_has:
            return True
    return False


# =============================================================================
# Outcome-referent resolution
#
#   - Polymarket: "Yes" refers to Outcome A Name (could be a literal "Yes",
#     or a team/candidate name for game/multi-outcome markets).
#   - Kalshi / PredictIt: question text is formatted "<context>: <side>",
#     where <side> after the final colon is what "Yes" actually means.
#     If the context contains "X vs Y", we can also recover the alternate
#     (No-side) name to confidently detect a flip. If not, we mark it
#     unknown rather than guess.
# =============================================================================

def last_word(name):
    if not isinstance(name, str) or not name.strip():
        return None
    return name.strip().split()[-1].lower()


def extract_after_colon(text):
    if isinstance(text, str) and ':' in text:
        return text.rsplit(':', 1)[-1].strip()
    return None


def extract_vs_pair(text):
    """If the part before the final colon contains 'X vs Y', return (X, Y)."""
    if not isinstance(text, str) or ':' not in text:
        return None
    before = text.rsplit(':', 1)[0]
    m = re.search(r'(.+?)\bvs\.?\b(.+)', before, flags=re.IGNORECASE)
    if not m:
        return None
    return m.group(1).strip(), m.group(2).strip()


def get_referent(text, poly_outcome_a=None, poly_outcome_b=None):
    """Returns (referent, alternate) for what 'Yes' means on this side."""
    if poly_outcome_a is not None:
        if not isinstance(poly_outcome_a, str) or poly_outcome_a.strip().lower() == 'yes':
            return None, None  # literal Yes/No market, no directional referent
        return poly_outcome_a, poly_outcome_b

    referent = extract_after_colon(text)
    if referent is None:
        return None, None

    pair = extract_vs_pair(text)
    alt = None
    if pair:
        a1, a2 = pair
        if last_word(a1) == last_word(referent):
            alt = a2
        elif last_word(a2) == last_word(referent):
            alt = a1
    return referent, alt


def alignment_status(ref_a, alt_a, ref_b, alt_b):
    if ref_a is None or ref_b is None:
        return 'aligned'  # one or both sides are literal Yes/No -- nothing to flip
    ra, rb = last_word(ref_a), last_word(ref_b)
    if ra == rb:
        return 'aligned'
    if alt_a is not None and last_word(alt_a) == rb:
        return 'flipped'
    if alt_b is not None and ra == last_word(alt_b):
        return 'flipped'
    return 'unknown'  # can't confirm -- don't risk trading on it


# =============================================================================
# Reusable pairwise matcher
# =============================================================================

def find_matches(
    df_a, name_col_a, yes_col_a, no_col_a, label_a,
    df_b, name_col_b, yes_col_b, no_col_b, label_b,
    poly_outcome_cols_a=None,
    poly_outcome_cols_b=None,
    end_date_col_a=None,
    end_date_col_b=None,
    url_col_a=None,
    url_col_b=None,
    similarity_threshold=0.92,
):
    strings_a = df_a[name_col_a].unique().tolist()
    strings_b = df_b[name_col_b].unique().tolist()
    print(f"Comparing {len(strings_a)} {label_a} markets against {len(strings_b)} {label_b} markets...")

    if not strings_a or not strings_b:
        empty = pd.DataFrame()
        return empty, empty

    model = PolyFuzz("TF-IDF")
    model.match(strings_a, strings_b)
    matches = model.get_matches()
    matches = matches[matches['Similarity'] >= similarity_threshold].copy()

    matches = matches[
        ~matches.apply(
            lambda r: has_conflict(r['From'], r['To'])
            or category_mismatch(r['From'], r['To'])
            or has_required_word_mismatch(r['From'], r['To']),
            axis=1
        )
    ].copy()

    a_market_col = f"{label_a}_Market"
    b_market_col = f"{label_b}_Market"
    matches = matches.rename(columns={"From": a_market_col, "To": b_market_col})

    merged = pd.merge(matches, df_a, left_on=a_market_col, right_on=name_col_a, how="inner")
    if name_col_a != a_market_col:
        merged = merged.drop(columns=[name_col_a])
    merged = pd.merge(
        merged, df_b, left_on=b_market_col, right_on=name_col_b, how="inner",
        suffixes=(f"_{label_a}", f"_{label_b}")
    )
    if name_col_b != b_market_col:
        merged = merged.drop(columns=[name_col_b])

    if merged.empty:
        return merged, merged

    # --- side alignment + outcome labels ---
    def _row_alignment_and_labels(row):
        oa_a = row.get(poly_outcome_cols_a[0]) if poly_outcome_cols_a else None
        ob_a = row.get(poly_outcome_cols_a[1]) if poly_outcome_cols_a else None
        oa_b = row.get(poly_outcome_cols_b[0]) if poly_outcome_cols_b else None
        ob_b = row.get(poly_outcome_cols_b[1]) if poly_outcome_cols_b else None

        ref_a, alt_a = get_referent(row[a_market_col], oa_a, ob_a)
        ref_b, alt_b = get_referent(row[b_market_col], oa_b, ob_b)
        status = alignment_status(ref_a, alt_a, ref_b, alt_b)

        a_yes_label = ref_a or "Yes"
        a_no_label = alt_a or "No"
        b_yes_label = ref_b or "Yes"
        b_no_label = alt_b or "No"

        if status == 'flipped':
            a_yes_label, a_no_label = a_no_label, a_yes_label

        return pd.Series({
            'Side_Alignment': status,
            'A_Yes_Label': a_yes_label,
            'A_No_Label': a_no_label,
            'B_Yes_Label': b_yes_label,
            'B_No_Label': b_no_label,
        })

    merged = pd.concat([merged, merged.apply(_row_alignment_and_labels, axis=1)], axis=1)

    unverified = merged[merged['Side_Alignment'] == 'unknown'].copy()
    merged = merged[merged['Side_Alignment'] != 'unknown'].copy()

    if merged.empty:
        return merged, unverified

    # --- standardized price columns (A/B, swapped for flipped rows) ---
    merged['A_Yes_Ask'] = merged[yes_col_a]
    merged['A_No_Ask'] = merged[no_col_a]
    merged['B_Yes_Ask'] = merged[yes_col_b]
    merged['B_No_Ask'] = merged[no_col_b]

    flipped = merged['Side_Alignment'] == 'flipped'
    merged.loc[flipped, ['A_Yes_Ask', 'A_No_Ask']] = merged.loc[flipped, ['A_No_Ask', 'A_Yes_Ask']].values

    merged['A_URL'] = merged[url_col_a] if url_col_a else None
    merged['B_URL'] = merged[url_col_b] if url_col_b else None

    # --- cost scenarios + which leg to actually buy on each platform ---
    merged['Yes_A_No_B'] = merged['A_Yes_Ask'] + merged['B_No_Ask']
    merged['Yes_B_No_A'] = merged['B_Yes_Ask'] + merged['A_No_Ask']
    merged['Best_Cost'] = merged[['Yes_A_No_B', 'Yes_B_No_A']].min(axis=1)

    use_a_yes = merged['Yes_A_No_B'] <= merged['Yes_B_No_A']

    merged['Action_A_Side'] = use_a_yes.map({True: 'Yes', False: 'No'})
    merged['Action_A_Label'] = merged['A_Yes_Label'].where(use_a_yes, merged['A_No_Label'])
    merged['Action_A_Price'] = merged['A_Yes_Ask'].where(use_a_yes, merged['A_No_Ask'])

    merged['Action_B_Side'] = use_a_yes.map({True: 'No', False: 'Yes'})
    merged['Action_B_Label'] = merged['B_No_Label'].where(use_a_yes, merged['B_Yes_Label'])
    merged['Action_B_Price'] = merged['B_No_Ask'].where(use_a_yes, merged['B_Yes_Ask'])

    merged['Max_ROI_%'] = (1.0 - merged['Best_Cost']) / merged['Best_Cost'] * 100

    merged['Platform_A'] = label_a
    merged['Platform_B'] = label_b
    merged = merged.rename(columns={a_market_col: 'A_Question', b_market_col: 'B_Question'})

    a_dates = pd.to_datetime(merged[end_date_col_a], utc=True, errors='coerce') if end_date_col_a else pd.Series(pd.NaT, index=merged.index)
    b_dates = pd.to_datetime(merged[end_date_col_b], utc=True, errors='coerce') if end_date_col_b else pd.Series(pd.NaT, index=merged.index)
    merged['End Date'] = a_dates.combine(
        b_dates,
        lambda x, y: min(d for d in (x, y) if pd.notna(d)) if pd.notna(x) or pd.notna(y) else pd.NaT
    )

    profitable = merged[merged['Best_Cost'] < 1.0].copy()

    output_cols = [
        'Platform_A', 'Platform_B', 'A_Question', 'B_Question', 'Similarity',
        'Action_A_Side', 'Action_A_Label', 'Action_A_Price',
        'Action_B_Side', 'Action_B_Label', 'Action_B_Price',
        'Side_Alignment', 'Best_Cost', 'Max_ROI_%', 'End Date',
        'A_URL', 'B_URL',
    ]
    return profitable[output_cols].copy(), unverified


# =============================================================================
# Top-level entry point
# =============================================================================

def run_arbitrage_scan(poly_df, kalshi_df, predictit_df, min_roi_pct=2.0, verbose=True):
    """
    Runs all three pairwise comparisons, combines them, filters to
    min_roi_pct+, and returns a list of dicts sorted by soonest end date
    first, then by ROI descending -- ready to serialize to JSON.
    """

    poly_clean = poly_df[
        ['Market Name', 'Poly Yes Ask', 'Poly No Ask',
         'Poly Outcome A Name', 'Poly Outcome B Name', 'Volume', 'Event URL', 'End Date']
    ].dropna(subset=['Market Name', 'Poly Yes Ask', 'Poly No Ask']) if not poly_df.empty else poly_df

    kalshi_clean = kalshi_df[
        ['Question', 'Kalshi Yes Ask', 'Kalshi No Ask', 'Volume', 'Ticker', 'Kalshi Close Time']
    ].dropna(subset=['Question', 'Kalshi Yes Ask', 'Kalshi No Ask']) if not kalshi_df.empty else kalshi_df

    predictit_clean = predictit_df[
        ['Market Name', 'PredictIt Yes Ask', 'PredictIt No Ask', 'Market URL']
    ].dropna(subset=['Market Name', 'PredictIt Yes Ask', 'PredictIt No Ask']) if not predictit_df.empty else predictit_df

    poly_kalshi_arbs, poly_kalshi_unverified = find_matches(
        poly_clean, 'Market Name', 'Poly Yes Ask', 'Poly No Ask', 'Poly',
        kalshi_clean, 'Question', 'Kalshi Yes Ask', 'Kalshi No Ask', 'Kalshi',
        poly_outcome_cols_a=('Poly Outcome A Name', 'Poly Outcome B Name'),
        end_date_col_a='End Date',
        end_date_col_b='Kalshi Close Time',
        url_col_a='Event URL',
        url_col_b='Ticker',
    )

    poly_predictit_arbs, poly_predictit_unverified = find_matches(
        poly_clean, 'Market Name', 'Poly Yes Ask', 'Poly No Ask', 'Poly',
        predictit_clean, 'Market Name', 'PredictIt Yes Ask', 'PredictIt No Ask', 'PredictIt',
        poly_outcome_cols_a=('Poly Outcome A Name', 'Poly Outcome B Name'),
        end_date_col_a='End Date',
        url_col_a='Event URL',
        url_col_b='Market URL',
    )

    kalshi_predictit_arbs, kalshi_predictit_unverified = find_matches(
        kalshi_clean, 'Question', 'Kalshi Yes Ask', 'Kalshi No Ask', 'Kalshi',
        predictit_clean, 'Market Name', 'PredictIt Yes Ask', 'PredictIt No Ask', 'PredictIt',
        end_date_col_a='Kalshi Close Time',
        url_col_a='Ticker',
        url_col_b='Market URL',
    )

    frames = [poly_kalshi_arbs, poly_predictit_arbs, kalshi_predictit_arbs]
    frames = [f for f in frames if f is not None and not f.empty]

    if not frames:
        return []

    combined = pd.concat(frames, ignore_index=True)
    combined = combined[combined['Max_ROI_%'] >= min_roi_pct].copy()

    # Sort: soonest-ending event first, then highest ROI first.
    # Opportunities with no resolvable end date sort to the bottom.
    combined['_end_sort'] = combined['End Date'].fillna(pd.Timestamp.max.tz_localize('UTC'))
    combined = combined.sort_values(
        by=['_end_sort', 'Max_ROI_%'], ascending=[True, False]
    ).drop(columns=['_end_sort']).reset_index(drop=True)

    if verbose:
        total_unverified = len(poly_kalshi_unverified) + len(poly_predictit_unverified) + len(kalshi_predictit_unverified)
        print(f"Found {len(combined)} arbitrage opportunities (>= {min_roi_pct}% ROI).")
        if total_unverified:
            print(f"Set aside {total_unverified} matches with unverifiable side alignment.")

    records = []
    for _, r in combined.iterrows():
        records.append({
            "platform_a": r['Platform_A'],
            "platform_b": r['Platform_B'],
            "question_a": r['A_Question'],
            "question_b": r['B_Question'],
            "similarity": round(float(r['Similarity']), 3) if pd.notna(r['Similarity']) else None,
            "action_a": {
                "side": r['Action_A_Side'],
                "outcome_label": r['Action_A_Label'],
                "price": round(float(r['Action_A_Price']), 4),
            },
            "action_b": {
                "side": r['Action_B_Side'],
                "outcome_label": r['Action_B_Label'],
                "price": round(float(r['Action_B_Price']), 4),
            },
            "side_alignment": r['Side_Alignment'],
            "best_cost": round(float(r['Best_Cost']), 4),
            "roi_pct": round(float(r['Max_ROI_%']), 2),
            "end_date": r['End Date'].isoformat() if pd.notna(r['End Date']) else None,
            "url_a": r['A_URL'],
            "url_b": r['B_URL'],
        })

    return records
