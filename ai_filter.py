"""
Smart rule-based filter — 100% free, no API needed.
Strictly filters to Freiburg im Breisgau area only (20km radius).
Checks TITLE only for location — not description (too unreliable).
"""

import logging

logger = logging.getLogger(__name__)

# Cities/PLZ within 20km of Freiburg — ACCEPTED
FREIBURG_AREA = [
    "freiburg", "freiburg im breisgau", "freiburg i.br",
    "merzhausen", "gundelfingen", "kirchzarten", "stegen",
    "buchenbach", "oberried", "horben", "wittnau", "bollschweil",
    "schallstadt", "bad krozingen", "breisach", "neuenburg",
    "müllheim", "staufen", "heitersheim", "hartheim", "vogtsburg",
    "ihringen", "merdingen", "bötzingen", "gottenheim", "bahlingen",
    "riegel", "endingen", "kenzingen", "waldkirch", "denzlingen",
    "teningen", "sexau", "elzach", "lehen", "littenweiler",
    "wiehre", "herdern", "haslach", "landwasser", "weingarten",
    "rieselfeld", "vauban", "betzenhausen", "opfingen", "tiengen",
    "munzingen", "waltershofen", "kappel", "ebnet", "günterstal",
    "zähringen", "mooswald", "brühl", "innenstadt", "altstadt",
    # PLZ codes for Freiburg and surroundings
    "79100", "79102", "79104", "79106", "79108", "79110", "79111",
    "79112", "79114", "79115", "79117", "79189", "79194", "79199",
    "79206", "79211", "79215", "79219", "79224", "79227", "79232",
    "79235", "79238", "79241", "79244", "79249", "79252", "79254",
    "79256", "79258", "79261", "79263", "79268", "79271", "79274",
    "79276", "79279", "79280", "79283", "79285", "79286", "79289",
    "79291", "79292", "79294", "79295", "79297", "79299",
]

# Cities FAR from Freiburg — REJECTED
FAR_CITIES = [
    "hamburg", "berlin", "münchen", "munich", "frankfurt", "köln",
    "cologne", "düsseldorf", "stuttgart", "dortmund", "essen",
    "bremen", "hannover", "nürnberg", "nuremberg", "leipzig",
    "dresden", "bochum", "wuppertal", "bielefeld", "bonn",
    "münster", "karlsruhe", "mannheim", "augsburg", "wiesbaden",
    "gelsenkirchen", "braunschweig", "chemnitz", "kiel", "aachen",
    "halle", "magdeburg", "krefeld", "mainz", "lübeck", "erfurt",
    "rostock", "kassel", "hagen", "hamm", "saarbrücken", "potsdam",
    "ludwigshafen", "heidelberg", "darmstadt", "trier", "regensburg",
    "ingolstadt", "würzburg", "ulm", "heilbronn", "konstanz",
    "pforzheim", "reutlingen", "tübingen", "ravensburg", "offenburg",
    "villingen", "schwenningen", "tuttlingen", "rottweil", "sigmaringen",
    "biberach", "friedrichshafen", "lindau", "norderstedt", "bornheim",
    "heddernheim", "westend", "harburg", "hanau", "offenbach",
    "aschaffenburg", "schweinfurt", "bamberg", "bayreuth", "landshut",
    "passau", "straubing", "langen", "mörfelden", "dreieich",
    "neu-isenburg", "bad homburg", "kronberg", "königstein",
    "oberursel", "eschborn", "bad vilbel", "nidderau", "büdingen",
]

POSITIVE_KEYWORDS = [
    "balkon", "terrasse", "aufzug", "fahrstuhl", "lift",
    "einbauküche", "ebk", "neubau", "renoviert", "modern",
    "ruhig", "hell", "sonnig", "parkplatz", "keller",
    "fußbodenheizung", "badewanne", "abstellraum",
]

NEGATIVE_KEYWORDS = [
    "erdgeschoss", "souterrain", "kein aufzug", "ohne aufzug",
    "befristet", "sanierungsbedürftig", "renovierungsbedürftig",
]


def is_in_freiburg_area(listing: dict) -> bool:
    """
    Check ONLY title and address — NOT description.
    Description often mentions other cities and causes false negatives.
    """
    # Only check title and address — most reliable fields
    addr  = listing.get("address", "").lower()
    title = listing.get("title", "").lower()
    check = f"{addr} {title}"

    # REJECT if far city found in title or address
    for city in FAR_CITIES:
        if city in check:
            return False

    # ACCEPT if Freiburg area city found
    for city in FREIBURG_AREA:
        if city in check:
            return True

    # If source is eBay/WG-Gesucht and they searched Freiburg — accept
    # (these scrapers already search Freiburg-specific URLs)
    source = listing.get("source", "").lower()
    if source in ["wg-gesucht", "ebay kleinanzeigen"]:
        return True

    return False


def score_listing(listing: dict, config: dict) -> dict:
    search = config["search"]
    score  = 5
    notes  = []

    price = listing.get("price", 0)
    size  = listing.get("size", 0)
    title = listing.get("title", "").lower()
    desc  = listing.get("description", "").lower()
    addr  = listing.get("address", "").lower()
    full  = f"{title} {desc} {addr}"

    # Price
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
            notes.append(f"OK price {price:.0f}€")
        else:
            score -= 2
            notes.append(f"Expensive {price:.0f}€")

    # Size
    min_size = search.get("min_size_m2", 40)
    max_size = search.get("max_size_m2", 70)
    if size > 0:
        if min_size <= size <= max_size:
            score += 1
        elif size > max_size:
            score += 2
        else:
            score -= 1

    # Balcony
    has_balcony = any(w in full for w in ["balkon", "terrasse"])
    if has_balcony:
        score += 1
        notes.append("Balcony ✅")

    # Elevator
    has_lift = any(w in full for w in ["aufzug", "fahrstuhl", "lift"])
    no_lift  = any(w in full for w in ["kein aufzug", "ohne aufzug"])
    if has_lift and not no_lift:
        score += 1
        notes.append("Elevator ✅")

    # City center
    if any(w in addr for w in ["altstadt", "innenstadt", "zentrum"]):
        score += 1
        notes.append("City center ✅")

    pos = [w for w in POSITIVE_KEYWORDS if w in full]
    if len(pos) >= 3:
        score += 1

    neg = [w for w in NEGATIVE_KEYWORDS if w in full]
    if neg:
        score -= 1

    score = max(1, min(10, score))

    parts = []
    if price > 0: parts.append(f"{price:.0f}€")
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
    search    = config["search"]
    blacklist = [kw.lower() for kw in search.get("keywords_blacklist", [])]
    min_score = config["ai"].get("min_score", 6)
    good = []

    for listing in listings:
        title_lower = listing.get("title", "").lower()
        desc_lower  = listing.get("description", "").lower()
        full_text   = f"{title_lower} {desc_lower}"

        # HARD FILTER 1: Location
        if not is_in_freiburg_area(listing):
            logger.info(f"⛔ Wrong location: {listing['title'][:50]} | {listing.get('address','')[:30]}")
            continue

        # HARD FILTER 2: Blacklist
        if any(kw in full_text for kw in blacklist):
            logger.info(f"⛔ Blacklisted: {listing['title'][:50]}")
            continue

        # HARD FILTER 3: Price
        price = listing.get("price", 0)
        if price and price > search["max_rent_warm"] + 100:
            logger.info(f"⛔ Too expensive ({price:.0f}€): {listing['title'][:50]}")
            continue

        # HARD FILTER 4: Size
        size = listing.get("size", 0)
        if size and size < search["min_size_m2"] - 5:
            logger.info(f"⛔ Too small ({size:.0f}m²): {listing['title'][:50]}")
            continue

        # Score it
        result = score_listing(listing, config)
        listing.update(result)

        if listing["ai_score"] >= min_score:
            good.append(listing)
            logger.info(f"✅ GOOD [{listing['ai_score']}/10]: {listing['title'][:50]} — {price:.0f}€")
        else:
            logger.info(f"❌ Skip [{listing['ai_score']}/10]: {listing['title'][:50]}")

    logger.info(f"✨ {len(good)} good listings from {len(listings)} total")
    return good
