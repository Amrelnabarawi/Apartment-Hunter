"""
Scrapers for German apartment listing sites.
Freiburg im Breisgau specific.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import random
import json
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

def get_page(url: str, delay: float = 2.0) -> BeautifulSoup | None:
    try:
        time.sleep(delay + random.uniform(0.5, 1.5))
        session = requests.Session()
        resp = session.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

def parse_price(text: str) -> float:
    """Extract numeric price from text like '850 €/Monat'"""
    if not text:
        return 0.0
    nums = re.findall(r"[\d.,]+", text.replace(".", "").replace(",", "."))
    for n in nums:
        try:
            val = float(n)
            if 100 < val < 10000:
                return val
        except:
            pass
    return 0.0

def parse_size(text: str) -> float:
    """Extract m² value from text"""
    if not text:
        return 0.0
    m = re.search(r"([\d,]+)\s*m", text.replace(",", "."))
    if m:
        try:
            return float(m.group(1))
        except:
            pass
    return 0.0

def parse_rooms(text: str) -> float:
    """Extract room count"""
    if not text:
        return 0.0
    m = re.search(r"([\d,]+)", text.replace(",", "."))
    if m:
        try:
            return float(m.group(1))
        except:
            pass
    return 0.0


# ─────────────────────────────────────────────────
# 1. ImmoScout24
# ─────────────────────────────────────────────────
def scrape_immoscout24(config: dict) -> List[Dict]:
    listings = []
    search = config["search"]
    min_size = search["min_size_m2"]
    max_size = search["max_size_m2"]
    min_rooms = search["min_rooms"]
    max_rooms = search["max_rooms"]
    max_warm = search["max_rent_warm"]

    # Search Freiburg + nearby cities
    cities_to_search = [
        ("freiburg-im-breisgau", "baden-wuerttemberg"),
        ("bad-krozingen", "baden-wuerttemberg"),
        ("breisach-am-rhein", "baden-wuerttemberg"),
        ("merzhausen", "baden-wuerttemberg"),
        ("kirchzarten", "baden-wuerttemberg"),
        ("staufen-im-breisgau", "baden-wuerttemberg"),
    ]

    for city_slug, state in cities_to_search:
        url = (
            f"https://www.immobilienscout24.de/Suche/de/{state}/"
            f"{city_slug}/wohnung-mieten"
            f"?numberofrooms={min_rooms}.0-{max_rooms}.0"
            f"&livingspace={min_size}.0-{max_size}.0"
            f"&price={search.get('min_rent_cold',500)}.0-{max_warm}.0"
            f"&sorting=2"
        )

        soup = get_page(url, delay=config["scraper"]["request_delay_seconds"])
        if not soup:
            continue

        # Try JSON in script tags first
        scripts = soup.find_all("script")
        for script in scripts:
            if script.string and "resultList" in (script.string or ""):
                try:
                    match = re.search(r'"resultList"\s*:\s*(\{.*?\})\s*[,}]', script.string, re.DOTALL)
                    if match:
                        data = json.loads(match.group(1))
                        results = data.get("resultlistEntries", [{}])[0].get("resultlistEntry", [])
                        for item in results[:20]:
                            exp = item.get("resultlist.realEstate", {})
                            price = exp.get("price", {}).get("value", 0)
                            size = exp.get("livingSpace", 0)
                            rooms = exp.get("numberOfRooms", 0)
                            title = exp.get("title", "")
                            listing_id = str(exp.get("@id", ""))
                            addr = exp.get("address", {})
                            address = f"{addr.get('street','')} {addr.get('houseNumber','')}, {addr.get('postcode','')} {addr.get('city','')}"
                            listing_url = f"https://www.immobilienscout24.de/expose/{listing_id}"
                            desc = exp.get("descriptionNote", "") + " " + exp.get("furnishingNote", "")
                            listings.append({
                                "id": f"is24_{listing_id}",
                                "title": title,
                                "price": price,
                                "size": size,
                                "rooms": rooms,
                                "address": address,
                                "url": listing_url,
                                "source": "ImmoScout24",
                                "description": desc,
                            })
                except Exception as e:
                    logger.error(f"ImmoScout24 JSON parse error ({city_slug}): {e}")

        # Fallback HTML
        if not any(l["source"] == "ImmoScout24" for l in listings):
            cards = soup.select("[data-item='result']")
            for card in cards[:20]:
                try:
                    title_el = card.select_one("h2, .result-list-entry__brand-title")
                    price_el = card.select_one(".result-list-entry__primary-criterion dd, [class*='price']")
                    link_el = card.select_one("a[href*='/expose/']")
                    if not link_el:
                        continue
                    href = link_el.get("href", "")
                    if href.startswith("/"):
                        href = "https://www.immobilienscout24.de" + href
                    listing_id = re.search(r"/expose/(\d+)", href)
                    listing_id = listing_id.group(1) if listing_id else href
                    text = card.get_text(separator=" ", strip=True)
                    listings.append({
                        "id": f"is24_{listing_id}",
                        "title": title_el.get_text(strip=True) if title_el else "",
                        "price": parse_price(price_el.get_text() if price_el else ""),
                        "size": parse_size(text),
                        "rooms": parse_rooms(text),
                        "address": city_slug.replace("-", " ").title(),
                        "url": href,
                        "source": "ImmoScout24",
                        "description": text[:500],
                    })
                except Exception as e:
                    logger.error(f"ImmoScout24 HTML card error: {e}")

    logger.info(f"ImmoScout24: found {len(listings)} listings across all cities")
    return listings


# ─────────────────────────────────────────────────
# 2. WG-Gesucht
# ─────────────────────────────────────────────────
def scrape_wggesucht(config: dict) -> List[Dict]:
    listings = []
    search = config["search"]
    # Freiburg city_id=41, radius=15km, type 2=Wohnung
    url = (
        f"https://www.wg-gesucht.de/wohnungen-in-Freiburg-im-Breisgau.41.2.1.0.html"
        f"?radius=15&rent_from={search.get('min_rent_cold',500)}"
        f"&rent_to={search['max_rent_warm']}"
        f"&sMin={search['min_size_m2']}&sMax={search['max_size_m2']}"
    )

    soup = get_page(url, delay=config["scraper"]["request_delay_seconds"])
    if not soup:
        return listings

    cards = soup.select(".wgg_card, .offer_list_item, [id^='liste-details']")
    for card in cards[:20]:
        try:
            title_el = card.select_one("h3 a, .truncate_title a")
            price_el = card.select_one(".middle b, [class*='price'], .noprint b")
            size_el = card.select_one("[class*='size'], .middle:last-child b")
            addr_el = card.select_one("[class*='address'], .col-xs-11")

            if not title_el:
                continue

            href = title_el.get("href", "")
            if href.startswith("/"):
                href = "https://www.wg-gesucht.de" + href

            listing_id = re.search(r"\.(\d+)\.html", href)
            listing_id = listing_id.group(1) if listing_id else href

            text = card.get_text(separator=" ", strip=True)
            price = parse_price(price_el.get_text() if price_el else text)
            size = parse_size(size_el.get_text() if size_el else text)

            listings.append({
                "id": f"wg_{listing_id}",
                "title": title_el.get_text(strip=True),
                "price": price,
                "size": size,
                "rooms": 2.0,
                "address": addr_el.get_text(strip=True) if addr_el else "Freiburg",
                "url": href,
                "source": "WG-Gesucht",
                "description": text[:500],
            })
        except Exception as e:
            logger.error(f"WG-Gesucht card error: {e}")

    logger.info(f"WG-Gesucht: found {len(listings)} listings")
    return listings


# ─────────────────────────────────────────────────
# 3. Immowelt
# ─────────────────────────────────────────────────
def scrape_immowelt(config: dict) -> List[Dict]:
    listings = []
    search = config["search"]
    min_size = search["min_size_m2"]
    max_size = search["max_size_m2"]
    max_warm = search["max_rent_warm"]

    url = (
        f"https://www.immowelt.de/liste/freiburg-im-breisgau/wohnungen/mieten"
        f"?ami={min_size}&xmi={max_size}&zi=2"
        f"&pma={max_warm}&umkreis=15"
        f"&sf=Erstellungsdatum&so=DESC"
    )

    soup = get_page(url, delay=config["scraper"]["request_delay_seconds"])
    if not soup:
        return listings

    cards = soup.select("[data-testid='serp-core-classified-card-testid'], .EstateItem")
    for card in cards[:20]:
        try:
            title_el = card.select_one("h2, [data-testid='classified-name'], .ellipsis")
            price_el = card.select_one("[data-testid='price'], .FactsView .Price")
            link_el = card.select_one("a[href*='/expose/']")

            if not link_el:
                link_el = card.select_one("a")
            if not link_el:
                continue

            href = link_el.get("href", "")
            if href.startswith("/"):
                href = "https://www.immowelt.de" + href

            listing_id = re.search(r"/expose/([a-zA-Z0-9]+)", href)
            listing_id = listing_id.group(1) if listing_id else href

            text = card.get_text(separator=" ", strip=True)
            listings.append({
                "id": f"iw_{listing_id}",
                "title": title_el.get_text(strip=True) if title_el else "Wohnung Freiburg",
                "price": parse_price(price_el.get_text() if price_el else text),
                "size": parse_size(text),
                "rooms": 2.0,
                "address": "Freiburg im Breisgau",
                "url": href,
                "source": "Immowelt",
                "description": text[:500],
            })
        except Exception as e:
            logger.error(f"Immowelt card error: {e}")

    logger.info(f"Immowelt: found {len(listings)} listings")
    return listings


# ─────────────────────────────────────────────────
# 4. eBay Kleinanzeigen
# ─────────────────────────────────────────────────
def scrape_ebay_kleinanzeigen(config: dict) -> List[Dict]:
    listings = []
    url = (
        "https://www.kleinanzeigen.de/s-wohnung-mieten/freiburg-im-breisgau/"
        "anzeige:angebote/preis::1400/c203l9445"
    )

    soup = get_page(url, delay=config["scraper"]["request_delay_seconds"])
    if not soup:
        return listings

    cards = soup.select("#srchrslt-adtable li.ad-listitem article, .aditem")
    for card in cards[:20]:
        try:
            title_el = card.select_one(".ellipsis, h2 a, [class*='title']")
            price_el = card.select_one(".aditem-main--middle--price-shipping--price, [class*='price']")
            link_el = card.select_one("a[href*='/s-anzeige/']")

            if not link_el and title_el:
                link_el = title_el.find_parent("a") or title_el.find("a")
            if not link_el:
                continue

            href = link_el.get("href", "")
            if href.startswith("/"):
                href = "https://www.kleinanzeigen.de" + href

            listing_id = re.search(r"/s-anzeige/[^/]+/(\d+)", href)
            listing_id = listing_id.group(1) if listing_id else href

            text = card.get_text(separator=" ", strip=True)
            listings.append({
                "id": f"ebay_{listing_id}",
                "title": title_el.get_text(strip=True) if title_el else "Wohnung",
                "price": parse_price(price_el.get_text() if price_el else text),
                "size": parse_size(text),
                "rooms": 2.0,
                "address": "Freiburg im Breisgau",
                "url": href,
                "source": "eBay Kleinanzeigen",
                "description": text[:500],
            })
        except Exception as e:
            logger.error(f"eBay error: {e}")

    logger.info(f"eBay Kleinanzeigen: found {len(listings)} listings")
    return listings


# ─────────────────────────────────────────────────
# 5. Wohnverdient.de
# ─────────────────────────────────────────────────
def scrape_wohnverdient(config: dict) -> List[Dict]:
    listings = []
    url = "https://wohnverdient.de/wohnungen/freiburg-im-breisgau"

    soup = get_page(url, delay=config["scraper"]["request_delay_seconds"])
    if not soup:
        return listings

    cards = soup.select(".listing-card, .property-item, article, [class*='listing']")
    for card in cards[:20]:
        try:
            title_el = card.select_one("h2, h3, [class*='title']")
            link_el = card.select_one("a[href]")
            if not link_el:
                continue

            href = link_el.get("href", "")
            if href.startswith("/"):
                href = "https://wohnverdient.de" + href

            text = card.get_text(separator=" ", strip=True)
            listing_id = re.sub(r"[^a-zA-Z0-9]", "", href)[-20:]

            listings.append({
                "id": f"wv_{listing_id}",
                "title": title_el.get_text(strip=True) if title_el else "Wohnung Freiburg",
                "price": parse_price(text),
                "size": parse_size(text),
                "rooms": 2.0,
                "address": "Freiburg im Breisgau",
                "url": href,
                "source": "Wohnverdient",
                "description": text[:500],
            })
        except Exception as e:
            logger.error(f"Wohnverdient error: {e}")

    logger.info(f"Wohnverdient: found {len(listings)} listings")
    return listings


# ─────────────────────────────────────────────────
# Main scraper runner
# ─────────────────────────────────────────────────
def run_all_scrapers(config: dict) -> List[Dict]:
    all_listings = []
    scrapers = [
        ("ImmoScout24",      scrape_immoscout24),
        ("WG-Gesucht",       scrape_wggesucht),
        ("Immowelt",         scrape_immowelt),
        ("eBay Kleinanzeigen", scrape_ebay_kleinanzeigen),
        ("Wohnverdient",     scrape_wohnverdient),
    ]
    for name, fn in scrapers:
        try:
            logger.info(f"Scraping {name}...")
            results = fn(config)
            all_listings.extend(results)
        except Exception as e:
            logger.error(f"Scraper {name} failed: {e}")

    return all_listings
