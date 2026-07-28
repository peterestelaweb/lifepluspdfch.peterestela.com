#!/usr/bin/env python3
"""Comprueba visualmente el catálogo local con Chromium y Playwright."""

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT = ROOT / "verificacion-playwright.png"
PRODUCT_SCREENSHOT = ROOT / "verificacion-producto-comprable.png"


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        headless=True,
        channel="chrome",
    )
    page = browser.new_page(viewport={"width": 590, "height": 980})
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
        "errors": errors,
        "screenshots": [str(SCREENSHOT), str(PRODUCT_SCREENSHOT)],
    }, ensure_ascii=False, indent=2))
    browser.close()
