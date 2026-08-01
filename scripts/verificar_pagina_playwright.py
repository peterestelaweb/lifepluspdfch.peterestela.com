#!/usr/bin/env python3
"""Comprueba visualmente el catálogo local con Chromium y Playwright."""

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT = ROOT / "verificacion-playwright.png"
PRODUCT_SCREENSHOT = ROOT / "verificacion-producto-comprable.png"
EXPECTED_ARTICLES = {
    "4145": ("107.75", "74.50"), "4146": ("107.75", "74.50"),
    "4147": ("114.00", "67.75"), "4148": ("114.00", "67.75"),
    "4149": ("110.75", "69.00"), "4150": ("110.75", "69.00"),
    "4156": ("90.00", "53.50"), "4158": ("90.00", "53.50"),
    "4168": ("316.00", "211.25"), "5019": ("202.00", "152.75"),
    "5046": ("256.00", "193.75"), "5279": ("264.50", "181.50"),
    "5395": ("169.75", "118.75"), "5397": ("221.75", "152.00"),
    "5401": ("93.25", "59.25"), "5402": ("89.00", "58.75"),
    "5403": ("93.25", "63.50"), "5404": ("90.00", "61.25"),
    "5405": ("92.00", "58.75"), "5406": ("90.00", "59.25"),
    "5516": ("117.25", "91.25"), "5692": ("171.50", "132.25"),
}
PACK_QUERIES = {
    "4168": "Sport Pack Sachet Berry", "5019": "Everyday Wellbeing Plus",
    "5046": "Everyday Wellbeing Gold Plus", "5279": "Sport Pack Canister Berry",
    "5395": "Getting Started", "5397": "Recovery Berry",
    "5516": "Everyday Wellbeing DE", "5692": "Everyday Wellbeing Gold DE",
}
GERMAN_PDF_CHECKS = {
    "2629": "fichas_producto/de/2629-PI_DE.pdf",
    "4144": "fichas_producto/de/4144-PI_DE.pdf",
    "4173": "fichas_producto/de/4173-PI_DE.pdf",
    "4174": "fichas_producto/de/4174-PI_DE.pdf",
    "5509": "fichas_producto/de/5509-PI_DE.pdf",
}


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        headless=True,
        channel="chrome",
    )
    page = browser.new_page(viewport={"width": 390, "height": 844})
    errors = []
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto((ROOT / "index.html").as_uri(), wait_until="networkidle")
    page.wait_for_selector(".product")
    result = page.evaluate(
        """() => ({
          products: document.querySelectorAll('.product').length,
          buyButtons: document.querySelectorAll('.shop-link').length,
          unavailable: document.querySelectorAll('.shop-unavailable').length,
          firstSix: [...document.querySelectorAll('.product')].slice(0, 6).map(card => ({
            title: card.querySelector('h2')?.textContent.trim(),
            sku: card.querySelector('.product-meta span')?.textContent.trim(),
            button: card.querySelector('.shop-link')?.textContent.trim() || null,
            href: card.querySelector('.shop-link')?.href || null,
            unavailable: card.querySelector('.shop-unavailable')?.textContent.trim() || null
          }))
        })"""
    )
    page.screenshot(path=str(SCREENSHOT))

    article_checks = {}
    for article, (price, ip) in EXPECTED_ARTICLES.items():
        page.locator("#searchInput").fill(article)
        card = page.locator(".product")
        sale_text = card.locator(".product-price").inner_text()
        href = card.locator(".shop-link").get_attribute("href")
        article_checks[article] = {
            "visibleProducts": card.count(),
            "priceAndIpCorrect": f"CHF {price}" in sale_text and f"IP {ip}" in sale_text,
            "cartUsesShop": href == "https://www.lifeplus.com/SHX4C7/ch/de/view-cart",
        }

    name_checks = {}
    for article, query in PACK_QUERIES.items():
        page.locator("#searchInput").fill(query)
        card = page.locator(f'.product:has-text("Art. {article}")')
        name_checks[article] = card.count() == 1

    page.locator('.filter[data-language="es"]').click()
    page.locator("#searchInput").fill("4168")
    pack_filter_check = {"hiddenWithoutSpanishPdf": page.locator(".product").count() == 0}
    page.locator('.filter[data-language="both"]').click()
    pack_filter_check["visibleInCombinedCatalog"] = page.locator(".product").count() == 1

    page.locator("#searchInput").fill("Lycopin Plus")
    lycopin_card = page.locator(".product")
    lycopin_check = {
        "visibleProducts": lycopin_card.count(),
        "article": lycopin_card.locator(".product-meta span").inner_text(),
        "hasSpanishPdf": lycopin_card.locator('.pdf-link:has-text("ES")').count() == 1,
        "hasGermanPdf": lycopin_card.locator('.pdf-link:has-text("DE")').count() == 1,
        "germanPdf": lycopin_card.locator('.pdf-link:has-text("DE")').get_attribute("href"),
        "hasUsNotice": "No existe una ficha equivalente en Estados Unidos" in lycopin_card.locator(".document-note").inner_text(),
    }

    german_pdf_checks = {}
    for article, expected_pdf in GERMAN_PDF_CHECKS.items():
        page.locator("#searchInput").fill(article)
        card = page.locator(".product")
        german_link = card.locator('.pdf-link:has-text("DE")')
        german_pdf_checks[article] = {
            "visibleProducts": card.count(),
            "hasGermanPdf": german_link.count() == 1,
            "germanPdfCorrect": german_link.get_attribute("href") == expected_pdf,
        }

    desktop = browser.new_page(viewport={"width": 1280, "height": 900})
    desktop.goto((ROOT / "index.html").as_uri(), wait_until="networkidle")
    desktop.locator("#searchInput").fill("4168")
    desktop_check = {
        "visibleProducts": desktop.locator(".product").count(),
        "article": desktop.locator(".product-meta span").inner_text(),
        "cartHref": desktop.locator(".shop-link").get_attribute("href"),
    }
    desktop.close()

    page.locator("#searchInput").fill("Wonder Gel")
    page.wait_for_timeout(300)
    buy_link = page.locator(".shop-link").first
    product_check = {
        "visibleProducts": page.locator(".product").count(),
        "buttonText": buy_link.inner_text(),
        "href": buy_link.get_attribute("href"),
    }
    page.screenshot(path=str(PRODUCT_SCREENSHOT))

    destination = browser.new_page()
    destination.goto(product_check["href"], wait_until="domcontentloaded")
    product_check["destinationUrl"] = destination.url
    product_check["destinationTitle"] = destination.title()
    product_check["opensProduct"] = "Wonder Gel" in product_check["destinationTitle"]
    destination.close()

    print(json.dumps({
        "result": result,
        "productCheck": product_check,
        "articleChecks": article_checks,
        "packNameChecks": name_checks,
        "packFilterCheck": pack_filter_check,
        "lycopinCheck": lycopin_check,
        "germanPdfChecks": german_pdf_checks,
        "mobileViewport": page.viewport_size,
        "desktopCheck": desktop_check,
        "errors": errors,
        "screenshots": [str(SCREENSHOT), str(PRODUCT_SCREENSHOT)],
    }, ensure_ascii=False, indent=2))
    browser.close()
