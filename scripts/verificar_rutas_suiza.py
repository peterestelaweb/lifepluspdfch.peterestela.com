#!/usr/bin/env python3
"""Audita cada tarjeta publicable contra el inventario actual de Lifeplus Suiza."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://www.lifeplus.com/SHX4C7/ch/de/web-page/products?tags=view_all"
DIRECT_BASE = "https://www.lifeplus.com/SHX4C7/ch/de/product-details/"
CART_URL = "https://www.lifeplus.com/SHX4C7/ch/de/view-cart"
REQUIRED_DIRECT = {"5828", "5830"}
EXPECTED_VISIBLE = 105


def embedded_array(source: str, name: str) -> list[dict]:
    marker = f"var {name} = "
    start = source.index(marker) + len(marker)
    return json.JSONDecoder().raw_decode(source[start:])[0]


def normalized(article: str) -> str:
    return str(int(article))


def main() -> None:
    commerce = json.loads((ROOT / "data/comercio-suiza.json").read_text(encoding="utf-8"))
    catalog = json.loads((ROOT / "data/catalogo-bilingue.json").read_text(encoding="utf-8"))

    request = urllib.request.Request(SOURCE, headers={"User-Agent": "Mozilla/5.0"})
    source = urllib.request.urlopen(request, timeout=45).read().decode("utf-8")
    public = {
        normalized(row["item_id"]): row
        for row in embedded_array(source, "productSet")
        if row.get("item_id")
    }
    secondary = {
        normalized(row["ShortProductID"]): row
        for row in embedded_array(source, "nmp")
        if row.get("ShortProductID") and str(row.get("IsAvailable")) == "1"
    }

    errors: list[str] = []
    visible_articles: set[str] = set()
    products = [*catalog["products"], *commerce["standalone_products"]]

    for product in products:
        sale = commerce["products"].get(product["sku"])
        if not sale or not (product.get("spanish") or product.get("german")):
            continue
        article = normalized(sale["article"])
        if article in visible_articles:
            continue
        visible_articles.add(article)

        row = public.get(article) or secondary.get(article)
        if not row:
            errors.append(f"{sale['article']}: no aparece en el inventario suizo actual")
            continue

        expected_price = float(row.get("price") or row.get("Price"))
        expected_ip = float(row.get("ip") or row.get("IP"))
        if abs(float(sale["price_chf"]) - expected_price) > 0.001:
            errors.append(f"{sale['article']}: precio {sale['price_chf']} != {expected_price:.2f}")
        if abs(float(sale["ip"]) - expected_ip) > 0.001:
            errors.append(f"{sale['article']}: IP {sale['ip']} != {expected_ip:.2f}")

        if article in public:
            expected_url = DIRECT_BASE + sale["article"]
            if sale["purchase"] != "direct" or sale["url"] != expected_url:
                errors.append(f"{sale['article']}: debe ser direct con {expected_url}")
        elif sale["purchase"] != "cart" or sale["url"] != CART_URL:
            errors.append(f"{sale['article']}: debe ser cart con {CART_URL}")

    if len(visible_articles) != EXPECTED_VISIBLE:
        errors.append(f"tarjetas visibles esperadas {EXPECTED_VISIBLE}, obtenidas {len(visible_articles)}")

    for article in REQUIRED_DIRECT:
        records = [record for record in commerce["products"].values() if record["article"] == article]
        if len(records) != 1:
            errors.append(f"{article}: se esperaba exactamente un registro comercial")
            continue
        record = records[0]
        if record["purchase"] != "direct" or record["url"] != DIRECT_BASE + article:
            errors.append(f"{article}: regresión de ruta directa")

    if errors:
        raise SystemExit("FAIL:\n- " + "\n- ".join(errors))

    print(
        f"PASS: {len(visible_articles)} referencias visibles coinciden en artículo, "
        "CHF, IP y ruta; 5828 y 5830 son direct en SHX4C7."
    )


if __name__ == "__main__":
    main()
