"""
AI-powered listing evaluator using Claude API.
Scores each listing 1–10 and gives a summary in Arabic.
"""

import anthropic
import json
import logging

logger = logging.getLogger(__name__)


def evaluate_listing(listing: dict, config: dict) -> dict:
    """
    Uses Claude to evaluate a listing and return:
    - score: 1–10
    - summary: short Arabic description
    - recommended: bool
    """
    client = anthropic.Anthropic(api_key=config["ai"]["anthropic_api_key"])

    search = config["search"]
    nearby = ", ".join(search.get("nearby_cities", ["Freiburg im Breisgau"]))
    prompt = f"""
أنت مساعد متخصص في تقييم إعلانات الشقق في ألمانيا.

معايير البحث:
- المنطقة: Freiburg im Breisgau وضواحيها في نطاق 15 كم (يُقبل: {nearby})
- عدد الغرف: {search['min_rooms']} – {search['max_rooms']} غرف
- المساحة: {search['min_size_m2']} – {search['max_size_m2']} متر مربع
- الإيجار البارد (Kaltmiete): {search.get('min_rent_cold',500)} – {search.get('max_rent_cold',700)} يورو
- الحد الأقصى الإيجار الساخن (Warmmiete): {search['max_rent_warm']} يورو
- بلكونة: {"مرغوبة جداً ✅" if search.get('prefer_balcony') else "غير مطلوبة"}
- أسانسير (إذا مش دور أرضي): {"مرغوب جداً ✅" if search.get('prefer_elevator') else "غير مطلوب"}
- وسائل النقل: المكان لازم يكون قريب من قطار أو باص يوصل لـ Freiburg

الإعلان:
العنوان: {listing.get('title', 'غير محدد')}
السعر: {listing.get('price', 0)} يورو
المساحة: {listing.get('size', 0)} م²
عدد الغرف: {listing.get('rooms', 0)}
العنوان: {listing.get('address', 'غير محدد')}
المصدر: {listing.get('source', '')}
الوصف: {listing.get('description', '')[:800]}

قيّم هذا الإعلان وأعطِ:
1. درجة من 1 إلى 10 (10 = مثالي)
   - نقّص درجة لو: السعر غالي، بعيد عن النقل، دور أرضي بدون تعليق، مفيش بلكونة
   - زوّد درجة لو: فيه بلكونة، فيه أسانسير، قريب من محطة، سعر مناسب
2. ملخص قصير بالعربية (جملتين بحد أقصى) يذكر أبرز مميزات أو عيوب + هل فيه بلكونة/أسانسير
3. هل توصي بالتواصل فوراً؟
4. نقل: هل المنطقة متوقع فيها قطار/باص لـ Freiburg؟ (true/false)

أجب فقط بـ JSON:
{{"score": 8, "summary": "شقة ممتازة بها بلكونة ...", "recommended": true, "good_transport": true}}

لا تكتب أي شيء خارج الـ JSON.
"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = message.content[0].text.strip()
        # Clean any markdown
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        return {
            "ai_score": int(result.get("score", 5)),
            "ai_summary": result.get("summary", ""),
            "recommended": result.get("recommended", False),
        }
    except Exception as e:
        logger.error(f"AI evaluation error: {e}")
        return {"ai_score": 5, "ai_summary": "تعذّر التقييم", "recommended": False}


def filter_listings(listings: list, config: dict) -> list:
    """Filter by basic criteria then AI-score remaining ones."""
    search = config["search"]
    blacklist = [kw.lower() for kw in search.get("keywords_blacklist", [])]
    min_score = config["ai"]["min_score"]

    good = []
    for listing in listings:
        title_lower = listing.get("title", "").lower()
        desc_lower = listing.get("description", "").lower()

        # Skip blacklisted keywords
        if any(kw in title_lower or kw in desc_lower for kw in blacklist):
            continue

        # Basic size filter (if we have data)
        size = listing.get("size", 0)
        if size and (size < search["min_size_m2"] - 5 or size > search["max_size_m2"] + 5):
            continue

        # Basic price filter
        price = listing.get("price", 0)
        if price and price > search["max_rent_warm"] + 200:
            continue

        # AI evaluation
        ai_result = evaluate_listing(listing, config)
        listing.update(ai_result)

        if listing["ai_score"] >= min_score:
            good.append(listing)
            logger.info(f"✅ GOOD [{listing['ai_score']}/10]: {listing['title']} – {listing['source']}")
        else:
            logger.info(f"❌ Skip [{listing['ai_score']}/10]: {listing['title']}")

    return good
