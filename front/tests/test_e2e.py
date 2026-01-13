from __future__ import annotations

import os

import pytest


@pytest.mark.e2e
def test_e2e_homepage_and_submit():
    """
    Test end-to-end (optionnel).
    - Nécessite un navigateur outillé (Playwright/Selenium) et le stack lancé.
    - Par défaut on skip si Playwright n'est pas installé.
    """
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception:
        pytest.skip("Playwright non installé (test e2e ignoré)")

    base_url = os.getenv("E2E_BASE_URL", "http://localhost")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(base_url, wait_until="domcontentloaded")
        page.fill("#username", "e2e")
        page.fill("#message", "hello")
        page.click("button[type=submit]")
        page.wait_for_load_state("domcontentloaded")

        # On vérifie au moins que la page répond et contient le titre
        assert "Forum Anonyme" in page.content()

        browser.close()

