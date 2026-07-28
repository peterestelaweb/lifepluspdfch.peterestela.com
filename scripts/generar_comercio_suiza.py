#!/usr/bin/env python3
"""Create the verified Swiss purchase layer for the bilingual PDF catalogue."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://www.lifeplus.com/SHX4C7/ch/de/web-page/products?tags=view_all"

PDF_TO_CH = {
    "1021":"1021", "170":"6695", "2629":"2629", "2630":"2630", "2631":"2631", "2632":"2632",
    "3415":"5828", "3443":"5825", "3446":"5827", "4033":"5821", "4095":"5871", "4129":"4129",
    "4130":"4130", "4131":"4131", "4132":"4132", "4133":"4133", "4134":"4134", "4144":"4144",
    "4173":"4173", "4174":"4174", "4998":"5049", "6108":"5826", "6112":"5823", "6134":"6134",
    "6140":"5834", "6192":"5829", "6237":"5822", "6618":"5413", "6648":"5869", "6651":"5870",
    "6654":"6654", "6656":"5874", "6658":"5875", "6673":"5879", "6678":"5884", "6679":"5885",
    "6687":"5887", "6688":"5888", "6689":"5889", "6692":"5390", "6697":"5894", "6698":"5895",
    "6699":"5896", "6861":"4000", "7796":"4655", "7797":"4656",
    "6003":"5044", "6603":"5403", "6604":"5404", "6800":"4145", "6801":"4146", "6601":"5401",
    "6602":"5402", "6806":"4149", "6807":"4150", "6644":"4158", "6605":"5405", "6606":"5406",
    "6805":"4148", "6802":"4147", "7883":"5521", "7884":"5522", "6104":"5011", "9600":"5006",
    "6133":"5010", "1012":"5591", "6109":"4443", "6355":"4008", "6132":"5003", "6500":"5792",
    "6193":"5028", "6122":"5004", "6111":"5008", "6107":"5032", "3447":"5047", "6113":"5500",
    "6063":"5096", "3457":"5509", "6127":"4463", "4999":"5000", "3538":"5388", "6653":"5872",
    "6141":"5012", "3428":"5009", "6102":"5496", "1032":"5038", "4421":"5534", "6041":"5708",
    "6343":"5789", "6124":"5036", "358":"4634", "3441":"5707", "6681":"5345", "6191":"5830",
    "6645":"4156", "3439":"5022", "1945":"0300", "6799":"5393", "6680":"5886",
}

# Packs confirmed in the secondary Swiss cart inventory. They do not have a
# single, unequivocal bilingual PDF, so they are published as commercial-only
# cards instead of being attached to one of their component documents.
COMMERCIAL_ONLY = {
    "4168": {
        "title": "Sport Pack Sachet Berry 30 ct",
        "description": "Pack deportivo en sobres, sabor frutos del bosque · Sportpaket mit Portionsbeuteln, Beerengeschmack",
        "category": "Packs Lifeplus",
    },
    "5019": {
        "title": "Everyday Wellbeing Plus DE",
        "description": "Pack Everyday Wellbeing Plus para Suiza · Everyday Wellbeing Plus Paket für die Schweiz",
        "category": "Packs Lifeplus",
    },
    "5046": {
        "title": "Everyday Wellbeing Gold Plus DE",
        "description": "Pack Everyday Wellbeing Gold Plus para Suiza · Everyday Wellbeing Gold Plus Paket für die Schweiz",
        "category": "Packs Lifeplus",
    },
    "5279": {
        "title": "Sport Pack Canister Berry DE",
        "description": "Pack deportivo en botes, sabor frutos del bosque · Sportpaket in Dosen, Beerengeschmack",
        "category": "Packs Lifeplus",
    },
    "5395": {
        "title": "Getting Started - Berry",
        "description": "Pack de inicio, sabor frutos del bosque · Einstiegspaket, Beerengeschmack",
        "category": "Packs Lifeplus",
    },
    "5397": {
        "title": "Recovery - Berry",
        "description": "Pack de recuperación, sabor frutos del bosque · Regenerationspaket, Beerengeschmack",
        "category": "Packs Lifeplus",
    },
    "5516": {
        "title": "Everyday Wellbeing DE",
        "description": "Pack Everyday Wellbeing para Suiza · Everyday Wellbeing Paket für die Schweiz",
        "category": "Packs Lifeplus",
    },
    "5692": {
        "title": "Everyday Wellbeing Gold DE",
        "description": "Pack Everyday Wellbeing Gold para Suiza · Everyday Wellbeing Gold Paket für die Schweiz",
        "category": "Packs Lifeplus",
    },
}

PHONE_OVERRIDES = {"5828", "5830"}
CART_URL = "https://www.lifeplus.com/SHX4C7/ch/de/view-cart"


def array(source: str, name: str) -> list[dict]:
    marker = f"var {name} = "
    start = source.index(marker) + len(marker)
    return json.JSONDecoder().raw_decode(source[start:])[0]


def main() -> None:
    req = urllib.request.Request(SOURCE, headers={"User-Agent":"Mozilla/5.0"})
    source = urllib.request.urlopen(req, timeout=45).read().decode("utf-8")
    direct = {str(x.get("item_id")):x for x in array(source,"productSet") if x.get("item_id")}
    phone = {str(x.get("ShortProductID")):x for x in array(source,"nmp") if x.get("ShortProductID")}
    products = {}
    missing = []
    for pdf_sku, article in PDF_TO_CH.items():
        row = direct.get(article) or phone.get(article)
        if not row:
            missing.append({"pdf_sku":pdf_sku,"article":article})
            continue
        is_direct = article in direct and article not in PHONE_OVERRIDES
        is_cart = article in phone and article not in PHONE_OVERRIDES
        products[pdf_sku] = {
            "article":article,
            "price_chf":f"{float(row.get('price') or row.get('Price')):.2f}",
            "ip":f"{float(row.get('ip') or row.get('IP')):.2f}",
            "purchase":"direct" if is_direct else ("cart" if is_cart else "phone"),
            "url":f"https://www.lifeplus.com/SHX4C7/ch/de/product-details/{article}" if is_direct else (CART_URL if is_cart else None),
        }
    standalone_products = []
    for article, metadata in COMMERCIAL_ONLY.items():
        row = phone.get(article)
        if not row:
            missing.append({"commercial_only":True,"article":article})
            continue
        key = f"ch-{article}"
        products[key] = {
            "article":article,
            "price_chf":f"{float(row.get('Price')):.2f}",
            "ip":f"{float(row.get('IP')):.2f}",
            "purchase":"cart",
            "url":CART_URL,
        }
        standalone_products.append({
            "sku":key,
            **metadata,
            "image":"",
            "spanish":"",
            "german":"",
            "commercial_only":True,
            "search":" ".join((metadata["title"], metadata["description"], article)).lower(),
        })
    payload={
        "shop_id":"SHX4C7",
        "phone_display":"0800 321 026",
        "phone_href":"tel:0800321026",
        "products":products,
        "standalone_products":standalone_products,
        "missing":missing,
    }
    text=json.dumps(payload,ensure_ascii=False,indent=2)
    (ROOT/"data/comercio-suiza.json").write_text(text+"\n",encoding="utf-8")
    (ROOT/"data/comercio-suiza.js").write_text(f"window.LIFEPLUS_COMMERCE = {text};\n",encoding="utf-8")
    print(f"Generated {len(products)} purchase records; missing: {missing}")


if __name__ == "__main__":
    main()
