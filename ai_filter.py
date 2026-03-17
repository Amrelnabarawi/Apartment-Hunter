"""
Smart rule-based filter — 100% free, no API needed.
Only shows apartments in Freiburg im Breisgau area (20km radius).
"""

import re
import logging

logger = logging.getLogger(__name__)

# ALL cities/areas within 20km of Freiburg — ONLY these are accepted
FREIBURG_AREA = [
    # Freiburg itself
    "freiburg", "freiburg im breisgau", "freiburg i.br", "freiburg i. br",
    # North
    "gundelfingen", "denzlingen", "teningen", "sexau", "gutach",
    "waldkirch", "elzach", "simonswald",
    # East
    "kirchzarten", "stegen", "buchenbach", "oberried", "horben",
    "wittnau", "bollschweil", "sölden", "pfaffenweiler",
    # South
    "schallstadt", "bad krozingen", "breisach", "bremgarten",
    "neuenburg", "müllheim", "auggen", "badenweiler", "sulzburg",
    "staufen", "ehrenstetten", "heitersheim",
    # West
    "hartheim", "vogtsburg", "ihringen", "merdingen", "bötzingen",
    "gottenheim", "bahlingen", "riegel", "endingen", "kenzingen",
    # Close suburbs
    "merzhausen", "gundelfingen", "lehen", "littenweiler",
    "wiehre", "herdern", "haslach", "landwasser", "weingarten",
    "rieselfeld", "vauban", "betzenhausen", "opfingen", "tiengen",
    "munzingen", "waltershofen", "kappel", "kappelrodeck",
    "ebnet", "kappel", "günterstal", "zähringen",
]

# Keywords that improve score
POSITIVE_KEYWORDS = [
    "balkon", "terrasse", "aufzug", "fahrstuhl", "lift",
    "einbauküche", "ebk", "neubau", "renoviert", "modern",
    "ruhig", "hell", "sonnig", "parkplatz", "keller",
    "fußbodenheizung", "badewanne", "abstellraum",
]

# Keywords that lower score
NEGATIVE_KEYWORDS = [
    "erdgeschoss", "souterrain", "kein aufzug", "ohne aufzug",
    "befristet", "sanierungsbedürftig", "renovierungsbedürftig",
]


def is_in_freiburg_area(listing: dict) -> bool:
    """Check if listing is in Freiburg area (20km radius)."""
    addr  = listing.get("address", "").lower()
    title = listing.get("title", "").lower()
    desc  = listing.get("description", "").lower()
    full  = f"{addr} {title} {desc}"

    # Must contain at least one Freiburg area city
    for city in FREIBURG_AREA:
        if city in full:
            return True
    return False


def score_listing(listing: dict, config: dict) -> dict:
    """Score listing 1-10 based on rules — no API needed."""
    search = config["search"]
    score  = 5
    notes  = []

    price = listing.get("price", 0)
    size  = listing.get("size", 0)
    title = listing.get("title", "").lower()
    desc  = listing.get("description", "").lower()
    addr  = listing.get("address", "").lower()
    full  = f"{title} {desc} {addr}"

    # ── Price ──────────────────────────────────────
    max_cold = search.get("max_rent_cold", 700)
    max_warm = search.get("max_rent_warm", 1000)

    if price > 0:
        if price <= max_cold:
            score += 2
            notes.append(f"Great price {price:.0f}€")
        elif price <= 850:
            score += 1
            notes.append(f"Good price {price:.0f}€")
        elif price <= max_warm:
            notes.append(f"Acceptable {price:.0f}€")
        else:
            score -= 2
            notes.append(f"Expensive {price:.0f}€")

    # ── Size ───────────────────────────────────────
    min_size = search.get("min_size_m2", 40)
    max_size = search.get("max_size_m2", 70)

    if size > 0:
        if min_size <= size <= max_size:
            score += 1
            notes.append(f"{size:.0f}m²")
        elif size > max_size:
            score += 2
            notes.append(f"Spacious {size:.0f}m²")
        else:
            score -= 1
            notes.append(f"Small {size:.0f}m²")

    # ── Balcony ────────────────────────────────────
    has_balcony = any(w in full for w in ["balkon", "terrasse"])
    if has_balcony:
        score += 1
        notes.append("Balcony ✅")
    elif search.get("prefer_balcony"):
        notes.append("No balcony")

    # ── Elevator ───────────────────────────────────
    has_lift = any(w in full for w in ["aufzug", "fahrstuhl", "lift"])
    no_lift  = any(w in full for w in ["kein aufzug", "ohne aufzug"])
    if has_lift and not no_lift:
        score += 1
        notes.append("Elevator ✅")

    # ── Freiburg city center bonus ─────────────────
    if any(w in addr for w in ["altstadt", "innenstadt", "zentrum", "city"]):
        score += 1
        notes.append("City center ✅")

    # ── Positive features ──────────────────────────
    pos = [w for w in POSITIVE_KEYWORDS if w in full]
    if len(pos) >= 3:
        score += 1

    # ── Negative features ──────────────────────────
    neg = [w for w in NEGATIVE_KEYWORDS if w in full]
    if neg:
        score -= 1

    score = max(1, min(10, score))

    # Build summary
    parts = []
    if price > 0: parts.append(f"{price:.0f}€/month")
    if size  > 0: parts.append(f"{size:.0f}m²")
    if has_balcony: parts.append("balcony")
    if has_lift and not no_lift: parts.append("elevator")
    if notes: parts.append(notes[0])

    summary = " • ".join(parts) if parts else "Apartment in Freiburg area"

    return {
        "ai_score": score,
        "ai_summary": summary,
        "recommended": score >= config["ai"].get("min_score", 6),
    }


def filter_listings(listings: list, config: dict) -> list:
    """Filter and score all listings — 100% free."""
    search    = config["search"]
    blacklist = [kw.lower() for kw in search.get("keywords_blacklist", [])]
    min_score = config["ai"].get("min_score", 6)
    good = []

    for listing in listings:
        title_lower = listing.get("title", "").lower()
        desc_lower  = listing.get("description", "").lower()
        full_text   = f"{title_lower} {desc_lower}"

        # ── HARD FILTER 1: Must be in Freiburg area ─
        if not is_in_freiburg_area(listing):
            logger.info(f"⛔ Wrong location: {listing['title']} — {listing.get('address','')}")
            continue

        # ── HARD FILTER 2: Blacklist keywords ───────
        if any(kw in full_text for kw in blacklist):
            logger.info(f"⛔ Blacklisted: {listing['title']}")
            continue

        # ── HARD FILTER 3: Price too high ───────────
        price = listing.get("price", 0)
        if price and price > search["max_rent_warm"] + 100:
            logger.info(f"⛔ Too expensive ({price:.0f}€): {listing['title']}")
            continue

        # ── HARD FILTER 4: Size wrong ────────────────
        size = listing.get("size", 0)
        if size and size < search["min_size_m2"] - 5:
            logger.info(f"⛔ Too small ({size:.0f}m²): {listing['title']}")
            continue

        # ── Score it ─────────────────────────────────
        result = score_listing(listing, config)
        listing.update(result)

        if listing["ai_score"] >= min_score:
            good.append(listing)
            logger.info(f"✅ GOOD [{listing['ai_score']}/10]: {listing['title']} — {listing.get('price',0):.0f}€ — {listing.get('address','')}")
        else:
            logger.info(f"❌ Skip [{listing['ai_score']}/10]: {listing['title']}")

    logger.info(f"✨ Filter complete: {len(good)} good listings from {len(listings)} total")
    return good
