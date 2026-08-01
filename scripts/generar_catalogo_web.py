#!/usr/bin/env python3
"""Genera el índice web bilingüe agrupando los documentos por producto/SKU."""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(
    "/Users/maykacenteno/Development/LIFEPLUSPDF CLONE/"
    "lifepluspdf.peterestela.com/data/pdf-index.json"
)
REGISTRY = ROOT / "fichas_producto/registro_bilingue.csv"
OUTPUT = ROOT / "data/catalogo-bilingue.json"
OUTPUT_JS = ROOT / "data/catalogo-bilingue.js"


def clean_title(value: str) -> str:
    value = re.sub(r"(?<!\d)\d{3,4}\s*-?\s*PI[\s_]*(?:ES|EN)\b", "", value, flags=re.I)
    value = re.sub(r"\bSOLO\s+(?:DISPONIBLE|EN)\b.*$", "", value, flags=re.I)
    value = re.sub(r"\s+", " ", value.replace(".pdf", "")).strip(" ._-")
    return value or "Ficha Lifeplus"


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value.lower())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in value if not unicodedata.combining(c))).strip()


def main() -> None:
    source_data = json.loads(SOURCE.read_text(encoding="utf-8"))
    metadata = {item["filename"]: item for item in source_data["pdfs"]}
    with REGISTRY.open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["sku"] or row["archivo_es"], []).append(row)

    products = []
    for key, group in grouped.items():
        preferred = max(
            group,
            key=lambda row: (
                bool(re.search(r"\d{3,4}-PI_ES", row["archivo_es"], re.I)),
                -len(row["archivo_es"]),
            ),
        )
        meta = metadata.get(preferred["archivo_es"], {})
        sku = preferred["sku"]
        title = clean_title(meta.get("title") or preferred["archivo_es"])
        image = meta.get("imagePath", "").replace("images/products/", "assets/products/")
        german = next((row["archivo_de"] for row in group if row["archivo_de"]), "")
        note = next((row.get("nota", "") for row in group if row.get("nota", "")), "")
        search = " ".join(
            [title, sku, meta.get("search_terms", ""), " ".join(meta.get("tags", []))]
        )
        product = {
            "sku": sku,
            "title": title,
            "description": f"Ficha técnica de {title}",
            "category": meta.get("category", "Productos Lifeplus"),
            "image": image,
            "spanish": f"fichas_producto/es/{preferred['archivo_es']}",
            "german": f"fichas_producto/de/{german}" if german else "",
            "search": norm(search),
        }
        if note:
            product["note"] = note
        products.append(product)

    products.sort(key=lambda item: item["title"].casefold())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    catalog = {"products": products}
    catalog_json = json.dumps(catalog, ensure_ascii=False, indent=2)
    OUTPUT.write_text(catalog_json, encoding="utf-8")
    OUTPUT_JS.write_text(
        f"window.LIFEPLUS_CATALOG = {catalog_json};\n", encoding="utf-8"
    )
    print(f"{len(products)} productos escritos en {OUTPUT}")


if __name__ == "__main__":
    main()
