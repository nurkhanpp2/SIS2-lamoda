import json
import re
from pathlib import Path
import pandas as pd


RAW = Path('data/raw_products.json')
CLEAN = Path('data/clean_products.csv')




def parse_price(p):
    if not isinstance(p, str):
        return None
    s = re.sub(r"[^0-9,\.]", "", p)
    s = s.replace(',', '.')
    try:
        return float(s)
    except Exception:
        return None




def normalize_text(s):
    if not s: return None
    return ' '.join(s.split()).strip()




def run():
    if not RAW.exists():
        raise FileNotFoundError(f"Raw file not found: {RAW}")


    with RAW.open('r', encoding='utf-8') as f:
        raw = json.load(f)


    df = pd.DataFrame(raw)


    df['name'] = df['name'].apply(normalize_text)
    df['brand'] = df['brand'].apply(normalize_text)
    df['price'] = df['price_raw'].apply(parse_price) if 'price_raw' in df.columns else None


    df = df[df['name'].notna() & df['price'].notna()]
    df = df.drop_duplicates(subset=['name', 'brand'], keep='first')


    print(f"Records after clean: {len(df)}")
    CLEAN.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN, index=False)
    print(f"Saved cleaned data -> {CLEAN}")




if __name__ == '__main__':
    run()
