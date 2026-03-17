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

# Rotate between different User-Agents to avoid blocking
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
]

def get_headers(referer: str = "") -> dict:
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
        **({"Referer": referer} if referer else {}),
    }

def get_page(url: str, delay: float = 2.0, referer: str = "") -> BeautifulSoup | None:
    try:
        time.sleep(delay + random.uniform(1.0, 2.5))
        session = requests.Session()
        # First visit homepage to get cookies
        domain = "/".join(url.split("/")[:3])
        try:
            session.get(domain, headers=get_headers(), timeout=10)
            time.sleep(random.uniform(0.5, 1.5))
        except:
            pass
        resp = session.get(url, headers=get_headers(referer=domain), timeout=20)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

def parse_price(text: str) -> float:
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
# 1. ImmoScout24 — using their API endpoint
# ─────────────────────────────────────────────────
def scrape_immoscout24(config: dict) -> List[Dict]:
    listings = []
    search = config["search"]

    # Use ImmoScout24 API directly — more reliable than HTML scraping
    api_url = (
        "https://api.immobilienscout24.de/restapi/api/search/v1.0/search/region"
        "?realestatetype=apartmentrent"
        "&geocodes=1276004001"  # Freiburg im Breisgau region code
        f"&livingspacemin={search['min_size_m2']}"
        f"&livingspacemax={search['max_size_m2']}"
        f"&pricefrom={search.get('min_rent_cold', 500)}"
        f"&priceto={search['max_rent_warm']}"
        "&numberofrooms=2.0-2.0"
        "&sorting=2"
        "&pagesize=20"
    )

    try:
        time.sleep(random.uniform(2, 4))
        session = requests.Session()
        # Visit homepage first to get cookies
        session.get("https://www.immobilienscout24.de", headers=get_headers(), timeout=15)
        time.sleep(random.uniform(1, 2))

        headers = get_headers(referer="https://www.immobilienscout24.de")
        headers["Accept"] = "application/json"

        resp = session.get(api_url, headers=headers, timeout=20)

        if resp.status_code == 200:
            data = resp.json()
            results = data.get("searchResponseModel", {}).get(
                "resultlist.resultlist", {}
            ).get("resultlistEntries", [{}])[0].get("resultlistEntry", [])

            for item in results[:20]:
                exp = item.get("resultlist.realEstate", {})
                price = exp.get("price", {}).get("value", 0)
                size = exp.get("livingSpace", 0)
                rooms = exp.get("numberOfRooms", 0)
                title = exp.get("title", "")
                listing_id = str(exp.get("@id", ""))
                addr = exp.get("address", {})
                address = f"{addr.get('street','')}, {addr.get('postcode','')} {addr.get('city','')}"
                listing_url = f"https://www.immobilienscout24.de/expose/{listing_id}"
                desc = exp.get("descriptionNote", "") + " " + exp.get("furnishingNote", "")
                listings.append({
                    "id": f"is24_{listing_id}",
                    "title": title,
                    "price": float(price),
                    "size": float(size),
                    "rooms": float(rooms),
                    "address": address,
                    "url": listing_url,
                    "source": "ImmoScout24",
                    "description": desc[:500],
                })
        else:
            logger.error(f"ImmoScout24 API returned {resp.status_code}")
            # Fallback: try HTML with better headers
            listings.extend(_scrape_immoscout24_html(config))

    except Exception as e:
        logger.error(f"ImmoScout24 API error: {e}")
        listings.extend(_scrape_immoscout24_html(config))

    logger.info(f"ImmoScout24: found {len(listings)} listings")
    return listings


def _scrape_immoscout24_html(config: dict) -> List[Dict]:
    """Fallback HTML scraper for ImmoScout24"""
    listings = []
    search = config["search"]
    url = (
        "https://www.immobilienscout24.de/Suche/de/baden-wuerttemberg/"
        "freiburg-im-breisgau/wohnung-mieten"
        f"?numberofrooms=2.0-2.0"
        f"&livingspace={search['min_size_m2']}.0-{search['max_size_m2']}.0"
        f"&price={search.get('min_rent_cold',500)}.0-{search['max_rent_warm']}.0"
        "&sorting=2"
    )

    soup = get_page(url, delay=3.0)
    if not soup:
        return listings

    # Try to extract from JSON in page
    for script in soup.find_all("script"):
        content = script.string or ""
        if "resultList" in content or "resultlistEntry" in content:
            try:
                match = re.search(r'"resultlistEntry"\s*:\s*(\[.*?\])', content, re.DOTALL)
                if match:
                    results = json.loads(match.group(1))
                    for item in results[:20]:
                        exp = item.get("resultlist.realEstate", {})
                        listing_id = str(exp.get("@id", ""))
                        if not listing_id:
                            continue
                        listings.append({
                            "id": f"is24_{listing_id}",
                            "title": exp.get("title", "Wohnung Freiburg"),
                            "price": float(exp.get("price", {}).get("value", 0)),
                            "size": float(exp.get("livingSpace", 0)),
                            "rooms": float(exp.get("numberOfRooms", 2)),
                            "address": "Freiburg im Breisgau",
                            "url": f"https://www.immobilienscout24.de/expose/{listing_id}",
                            "source": "ImmoScout24",
                            "description": exp.get("descriptionNote", "")[:500],
                        })
            except:
                pass
    return listings


# ─────────────────────────────────────────────────
# 2. WG-Gesucht
# ─────────────────────────────────────────────────
def scrape_wggesucht(config: dict) -> List[Dict]:
    listings = []
    search = config["search"]
    url = (
        "https://www.wg-gesucht.de/wohnungen-in-Freiburg-im-Breisgau.41.2.1.0.html"
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
            size_el  = card.select_one("[class*='size'], .middle:last-child b")
            addr_el  = card.select_one("[class*='address'], .col-xs-11")
            if not title_el:
                continue
            href = title_el.get("href", "")
            if href.startswith("/"):
                href = "https://www.wg-gesucht.de" + href
            listing_id = re.search(r"\.(\d+)\.html", href)
            listing_id = listing_id.group(1) if listing_id else href[-20:]
            text  = card.get_text(separator=" ", strip=True)
            listings.append({
                "id": f"wg_{listing_id}",
                "title": title_el.get_text(strip=True),
                "price": parse_price(price_el.get_text() if price_el else text),
                "size":  parse_size(size_el.get_text()  if size_el  else text),
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
    url = (
        "https://www.immowelt.de/liste/freiburg-im-breisgau/wohnungen/mieten"
        f"?ami={search['min_size_m2']}&xmi={search['max_size_m2']}&zi=2"
        f"&pma={search['max_rent_warm']}&umkreis=15"
        "&sf=Erstellungsdatum&so=DESC"
    )

    soup = get_page(url, delay=config["scraper"]["request_delay_seconds"])
    if not soup:
        return listings

    cards = soup.select("[data-testid='serp-core-classified-card-testid'], .EstateItem")
    for card in cards[:20]:
        try:
            title_el = card.select_one("h2, [data-testid='classified-name'], .ellipsis")
            price_el = card.select_one("[data-testid='price'], .FactsView .Price")
            link_el  = card.select_one("a[href*='/expose/']") or card.select_one("a")
            if not link_el:
                continue
            href = link_el.get("href", "")
            if href.startswith("/"):
                href = "https://www.immowelt.de" + href
            listing_id = re.search(r"/expose/([a-zA-Z0-9]+)", href)
            listing_id = listing_id.group(1) if listing_id else href[-20:]
            text = card.get_text(separator=" ", strip=True)
            listings.append({
                "id": f"iw_{listing_id}",
                "title": title_el.get_text(strip=True) if title_el else "Wohnung Freiburg",
                "price": parse_price(price_el.get_text() if price_el else text),
                "size":  parse_size(text),
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
            link_el  = card.select_one("a[href*='/s-anzeige/']")
            if not link_el and title_el:
                link_el = title_el.find_parent("a") or title_el.find("a")
            if not link_el:
                continue
            href = link_el.get("href", "")
            if href.startswith("/"):
                href = "https://www.kleinanzeigen.de" + href
            listing_id = re.search(r"/s-anzeige/[^/]+/(\d+)", href)
            listing_id = listing_id.group(1) if listing_id else href[-20:]
            text = card.get_text(separator=" ", strip=True)
            listings.append({
                "id": f"ebay_{listing_id}",
                "title": title_el.get_text(strip=True) if title_el else "Wohnung",
                "price": parse_price(price_el.get_text() if price_el else text),
                "size":  parse_size(text),
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
# 5. Wohnverdient — fixed URL + POST support
# ─────────────────────────────────────────────────
def scrape_wohnverdient(config: dict) -> List[Dict]:
    listings = []
    search = config["search"]

    urls_to_try = [
        "https://wohnverdient.de/wohnungen/freiburg-im-breisgau",
        "https://wohnverdient.de/mieten/freiburg",
        "https://wohnverdient.de/wohnungen?city=freiburg",
    ]

    soup = None
    for url in urls_to_try:
        try:
            time.sleep(random.uniform(2, 4))
            session = requests.Session()
            session.get("https://wohnverdient.de", headers=get_headers(), timeout=15)
            time.sleep(random.uniform(1, 2))
            resp = session.get(url, headers=get_headers(referer="https://wohnverdient.de"), timeout=20)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                break
            else:
                logger.error(f"Wohnverdient {url}: {resp.status_code}")
        except Exception as e:
            logger.error(f"Wohnverdient {url}: {e}")

    if not soup:
        logger.info("Wohnverdient: could not access site, skipping")
        return listings

    cards = soup.select(".listing-card, .property-item, article, [class*='listing'], [class*='property']")
    for card in cards[:20]:
        try:
            title_el = card.select_one("h2, h3, [class*='title']")
            link_el  = card.select_one("a[href]")
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
                "size":  parse_size(text),
                "rooms": 2.0,
                "address": "Freiburg im Breisgau",
                "url": href,
                "source": "Wohnverdient",
                "description": text[:500],
            })
        except Exception as e:
            logger.error(f"Wohnverdient card error: {e}")

    logger.info(f"Wohnverdient: found {len(listings)} listings")
    return listings


# ─────────────────────────────────────────────────
# Main runner
# ─────────────────────────────────────────────────
def run_all_scrapers(config: dict) -> List[Dict]:
    all_listings = []
    scrapers = [
        ("ImmoScout24",        scrape_immoscout24),
        ("WG-Gesucht",         scrape_wggesucht),
        ("Immowelt",           scrape_immowelt),
        ("eBay Kleinanzeigen", scrape_ebay_kleinanzeigen),
        ("Wohnverdient",       scrape_wohnverdient),
    ]
    for name, fn in scrapers:
        try:
            logger.info(f"Scraping {name}...")
            results = fn(config)
            all_listings.extend(results)
        except Exception as e:
            logger.error(f"Scraper {name} failed: {e}")
    return all_listings
