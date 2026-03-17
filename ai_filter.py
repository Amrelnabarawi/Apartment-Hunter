"""
Smart rule-based filter — 100% free, no API needed.
Filters apartments by price, size, rooms, location, and keywords.
Scores each listing 1-10 based on how well it matches preferences.
"""

import re
import logging

logger = logging.getLogger(__name__)

# Keywords that make a listing better
POSITIVE_KEYWORDS = [
    "balkon", "balcon", "terrasse", "aufzug", "fahrstuhl", "lift",
    "einbauküche", "EBK", "neubau", "renoviert", "modern", "ruhig",
    "hell", "sonnig", "parkplatz", "stellplatz", "keller", "garten",
    "fußbodenheizung", "badewanne", "dusche", "abstellraum",
]

# Keywords that make a listing worse
NEGATIVE_KEYWORDS = [
    "erdgeschoss", "EG", "souterrain", "kein aufzug", "ohne aufzug",
    "befristet", "zwischenmiete", "untermiete", "möbliert auf zeit",
    "sanierungsbedürftig", "renovierungsbedürftig",
]

# Cities/areas within 15km of Freiburg — all acceptable
FREIBURG_AREA = [
    "freiburg", "merzhausen", "gundelfingen", "kirchzarten", "staufen",
    "breisach", "bad krozingen", "müllheim", "neuenburg", "hartheim",
    "vogtsburg", "ihringen", "merdingen", "bötzingen", "gottenheim",
    "bahlingen", "riegel", "endingen", "kenzingen", "waldkirch",
    "denzlingen", "teningen", "sexau", "gutach", "elzach",
    "schallstadt", "offnadingen", "wittnau", "horben", "oberried",
]


def score_listing(listing: dict, config: dict) -> dict:
    """
    Score a listing 1-10 based on rules — no API needed.
    Returns updated listing with ai_score and ai_summary.
    """
    search = config["search"]
    score = 5  # Start at 5
    notes = []

    price = listing.get("price", 0)
    size  = listing.get("size", 0)
    rooms = listing.get("rooms", 0)
    title = listing.get("title", "").lower()
    desc  = listing.get("description", "").lower()
    addr  = listing.get("address", "").lower()
    full_text = f"{title} {desc} {addr}"

    # ── Price scoring ──────────────────────────────
    min_cold = search.get("min_rent_cold", 500)
    max_cold = search.get("max_rent_cold", 700)
    max_warm = search.get("max_rent_warm", 1000)

    if price > 0:
        if price <= max_cold:
            score += 2
            notes.append(f"Great price: {price:.0f}€")
        elif price <= (max_cold + max_warm) / 2:
            score += 1
            notes.append(f"Good price: {price:.0f}€")
        elif price <= max_warm:
            notes.append(f"Acceptable price: {price:.0f}€")
        else:
            score -= 2
            notes.append(f"Expensive: {price:.0f}€")

    # ── Size scoring ───────────────────────────────
    min_size = search.get("min_size_m2", 40)
    max_size = search.get("max_size_m2", 70)

    if size > 0:
        if min_size <= size <= max_size:
            score += 1
            notes.append(f"Good size: {size:.0f}m²")
        elif size > max_size:
            score += 2
            notes.append(f"Spacious: {size:.0f}m²")
        else:
            score -= 1
            notes.append(f"Small: {size:.0f}m²")

    # ── Balcony ────────────────────────────────────
    has_balcony = any(w in full_text for w in ["balkon", "terrasse", "balcon"])
    if has_balcony:
        score += 1
        notes.append("Has balcony ✅")
    elif search.get("prefer_balcony"):
        score -= 1
        notes.append("No balcony mentioned")

    # ── Elevator ───────────────────────────────────
    has_elevator = any(w in full_text for w in ["aufzug", "fahrstuhl", "lift"])
    no_elevator  = any(w in full_text for w in ["kein aufzug", "ohne aufzug", "kein fahrstuhl"])
    if has_elevator and not no_elevator:
        score += 1
        notes.append("Has elevator ✅")
    elif no_elevator and search.get("prefer_elevator"):
        score -= 1
        notes.append("No elevator")

    # ── Location ───────────────────────────────────
    in_freiburg_area = any(city in addr for city in FREIBURG_AREA)
    if in_freiburg_area:
        score += 1
        notes.append("Good location ✅")

    if "freiburg" in addr and ("altstadt" in addr or "innenstadt" in addr or "zentrum" in addr):
        score += 1
        notes.append("City center ✅")

    # ── Positive keywords ──────────────────────────
    pos_found = [w for w in POSITIVE_KEYWORDS if w.lower() in full_text]
    if len(pos_found) >= 3:
        score += 1
        notes.append(f"Many features: {', '.join(pos_found[:3])}")

    # ── Negative keywords ──────────────────────────
    neg_found = [w for w in NEGATIVE_KEYWORDS if w.lower() in full_text]
    if neg_found:
        score -= 1
        notes.append(f"Drawbacks: {', '.join(neg_found[:2])}")

    # ── Ground floor penalty ───────────────────────
    is_ground = any(w in full_text for w in ["erdgeschoss", "eg ", "souterrain"])
    if is_ground and search.get("prefer_elevator"):
        score -= 1
        notes.append("Ground floor")

    # ── Keep score between 1-10 ────────────────────
    score = max(1, min(10, score))

    # ── Build summary ──────────────────────────────
    summary_parts = []
    if price > 0:
        summary_parts.append(f"{price:.0f}€/month")
    if size > 0:
        summary_parts.append(f"{size:.0f}m²")
    if has_balcony:
        summary_parts.append("balcony")
    if has_elevator and not no_elevator:
        summary_parts.append("elevator")
    if notes:
        summary_parts.append(notes[0])

    summary = " • ".join(summary_parts) if summary_parts else "Good apartment in Freiburg area"

    return {
        "ai_score": score,
        "ai_summary": summary,
        "recommended": score >= config["ai"].get("min_score", 6),
    }


def filter_listings(listings: list, config: dict) -> list:
    """Filter and score all listings — 100% free, no API."""
    search    = config["search"]
    blacklist = [kw.lower() for kw in search.get("keywords_blacklist", [])]
    min_score = config["ai"].get("min_score", 6)

    good = []

    for listing in listings:
        title_lower = listing.get("title", "").lower()
        desc_lower  = listing.get("description", "").lower()
        full_text   = f"{title_lower} {desc_lower}"

        # ── Hard filters — skip immediately ────────
        # Blacklist keywords
        if any(kw in full_text for kw in blacklist):
            logger.info(f"⛔ Blacklisted: {listing['title']}")
            continue

        # Price too high
        price = listing.get("price", 0)
        if price and price > search["max_rent_warm"] + 100:
            logger.info(f"⛔ Too expensive ({price}€): {listing['title']}")
            continue

        # Size too small or too large (if we have data)
        size = listing.get("size", 0)
        if size and size < search["min_size_m2"] - 5:
            logger.info(f"⛔ Too small ({size}m²): {listing['title']}")
            continue
        if size and size > search["max_size_m2"] + 10:
            logger.info(f"⛔ Too large ({size}m²): {listing['title']}")
            continue

        # ── Score the listing ──────────────────────
        result = score_listing(listing, config)
        listing.update(result)

        if listing["ai_score"] >= min_score:
            good.append(listing)
            logger.info(f"✅ GOOD [{listing['ai_score']}/10]: {listing['title']} — {listing.get('price',0):.0f}€ — {listing['source']}")
        else:
            logger.info(f"❌ Skip [{listing['ai_score']}/10]: {listing['title']}")

    logger.info(f"✨ Filter complete: {len(good)} good listings from {len(listings)} total")
    return good
