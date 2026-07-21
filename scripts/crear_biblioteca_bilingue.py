#!/usr/bin/env python3
"""Copia las fichas ES existentes y descarga las fichas DE oficiales de Lifeplus."""

from __future__ import annotations

import csv
import json
import re
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ES = Path(
    "/Users/maykacenteno/Development/LIFEPLUSPDF CLONE/"
    "lifepluspdf.peterestela.com/pdfs"
)
SOURCE_INDEX = SOURCE_ES.parent / "data" / "pdf-index.json"
LIBRARY = ROOT / "fichas_producto"
ES_DIR = LIBRARY / "es"
DE_DIR = LIBRARY / "de"
REGISTRY = LIBRARY / "registro_bilingue.csv"
BASE_DE = "https://ww2.lifeplus.com/media/pdf/piSheets/US/{sku}-PI_DE.pdf"


def load_index_skus() -> dict[str, str]:
    if not SOURCE_INDEX.is_file():
        return {}
    data = json.loads(SOURCE_INDEX.read_text(encoding="utf-8"))
    result = {}
    for item in data.get("pdfs", []):
        match = re.search(r"prodpic_(\d+)_", item.get("imagePath", ""))
        if match:
            result[item["filename"]] = match.group(1)
    return result


def extract_sku(name: str, index_skus: dict[str, str]) -> str:
    match = re.search(r"(?<!\d)(\d{3,4})-PI_(?:ES|EN)", name, re.I)
    if match:
        return match.group(1)
    numbers = re.findall(r"(?<!\d)(\d{3,4})(?!\d)", name)
    return numbers[-1] if numbers else index_skus.get(name, "")


def download_de(sku: str) -> tuple[str, str, str]:
    url = BASE_DE.format(sku=sku)
    target = DE_DIR / f"{sku}-PI_DE.pdf"
    if target.exists() and target.read_bytes()[:5] == b"%PDF-":
        return sku, "descargado", url

    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
            final_url = response.geturl()
        if data[:5] != b"%PDF-":
            return sku, "no_disponible", final_url
        target.write_bytes(data)
        return sku, "descargado", final_url
    except Exception as exc:  # deja el fallo trazable en el CSV
        return sku, f"error: {type(exc).__name__}", url


def main() -> None:
    if not SOURCE_ES.is_dir():
        raise SystemExit(f"No existe la carpeta fuente: {SOURCE_ES}")

    ES_DIR.mkdir(parents=True, exist_ok=True)
    DE_DIR.mkdir(parents=True, exist_ok=True)

    spanish_files = sorted(SOURCE_ES.glob("*.pdf"), key=lambda path: path.name.casefold())
    index_skus = load_index_skus()
    for source in spanish_files:
        shutil.copy2(source, ES_DIR / source.name)

    skus = sorted(
        {extract_sku(path.name, index_skus) for path in spanish_files} - {""}, key=int
    )
    de_results: dict[str, tuple[str, str]] = {}
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(download_de, sku): sku for sku in skus}
        for future in as_completed(futures):
            sku, status, url = future.result()
            de_results[sku] = (status, url)

    with REGISTRY.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["sku", "archivo_es", "archivo_de", "estado_de", "url_oficial_de"]
        )
        for source in spanish_files:
            sku = extract_sku(source.name, index_skus)
            status, url = de_results.get(sku, ("sin_sku", ""))
            de_name = f"{sku}-PI_DE.pdf" if status == "descargado" else ""
            writer.writerow([sku, source.name, de_name, status, url])

    downloaded = sum(status == "descargado" for status, _ in de_results.values())
    unavailable = sum(status == "no_disponible" for status, _ in de_results.values())
    print(f"Español: {len(spanish_files)} PDFs")
    print(f"Alemán: {downloaded} PDFs")
    print(f"SKU sin ficha alemana: {unavailable}")
    print(f"Registro: {REGISTRY}")


if __name__ == "__main__":
    main()
