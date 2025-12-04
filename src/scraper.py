import json
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright


OUT_FILE = Path("data/raw_products.json")
TARGET_URL = "https://www.lamoda.kz/c/3949/default-sport_men_run/"
DESIRED_COUNT = 120


CARD_SELECTOR = "div.x-product-card__card"
NAME_SELECTOR = ".x-product-card-description__product-name"
BRAND_SELECTOR = ".x-product-card-description__brand-name"
PRICE_SELECTOR = ".x-product-card-description__price-single, .x-product-card-description__price-discounted"




def parse_card(el):
    def safe_text(sel):
        try:
            node = el.query_selector(sel)
            return node.inner_text().strip() if node else None
        except:
            return None

    # URL
    url = None
    try:
        a = el.query_selector("a[href*='/p/']")
        if a:
            href = a.get_attribute("href")
            url = f"https://www.lamoda.kz{href}"
    except:
        pass

    # Name / Brand
    name = safe_text(NAME_SELECTOR)
    brand = safe_text(BRAND_SELECTOR)

    # Price
    price_raw = None
    for sel in [
        ".x-product-card-description__price-new",
        ".x-product-card-description__price-single",
        ".x-product-card-description__price-discounted",
        ".x-product-card-description__price",
        ".x-product-card-description__price-old"
    ]:
        txt = safe_text(sel)
        if txt:
            price_raw = txt
            break

    return {
        'product_url': url,
        'name': name,
        'brand': brand,
        'price_raw': price_raw,
        'scraped_at': datetime.utcnow().isoformat()
    }




def scroll_and_collect(page, desired_count=DESIRED_COUNT, pause=1.0, max_attempts=80):
    items = {}
    attempts = 0
    last_len = 0


    while len(items) < desired_count and attempts < max_attempts:
        cards = page.query_selector_all(CARD_SELECTOR)
        for c in cards:
            try:
                rec = parse_card(c)
                key = rec.get('product_url') or (rec.get('name') + (rec.get('brand') or ''))
                if key and key not in items:
                    items[key] = rec
            except Exception:
                continue

        page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
        time.sleep(pause)
        attempts += 1
        time.sleep(0.5)
        last_len = len(items)


    return list(items.values())




def run():
  OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
  with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    page = context.new_page()
    page.goto(TARGET_URL, wait_until='networkidle')


    try:
        pass # клик по баннеру cookies при необходимости
    except Exception:
        pass
  

    data = scroll_and_collect(page)
    with OUT_FILE.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


    print(f"Scraped {len(data)} records -> {OUT_FILE}")
    browser.close()




if __name__ == '__main__':
    run()
