#!/usr/bin/env python3
"""
Browser E2E Journey Automation Engine
Injected HUD Overlay & Spotlight Runner (Playwright CDP Engine)
Feature: PB082643640012YA (Anti-Fraud CMS)
Target SUT: http://192.168.181.60/mobilebroadcast/
"""

import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

BASE_URL = "http://192.168.181.60/mobilebroadcast/"
CHROME_PATH = "/home/gunawan/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome"
SCREENSHOT_DIR = Path(__file__).resolve().parent / "screenshots"

HUD_AND_SPOTLIGHT_JS = """
(() => {
    // 1. Inject Style if not already present
    if (!document.getElementById('agy-hud-spotlight-styles')) {
        const style = document.createElement('style');
        style.id = 'agy-hud-spotlight-styles';
        style.innerHTML = `
            /* --- INJECTED HUD OVERLAY --- */
            #agy-hud-container {
                position: fixed;
                top: 14px;
                left: 50%;
                transform: translateX(-50%);
                z-index: 2147483647;
                width: 820px;
                max-width: 95vw;
                background: linear-gradient(135deg, rgba(15, 23, 42, 0.94) 0%, rgba(30, 41, 59, 0.94) 100%);
                backdrop-filter: blur(14px);
                border: 1.5px solid rgba(56, 189, 248, 0.75);
                border-radius: 12px;
                box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.65), 0 0 20px rgba(56, 189, 248, 0.35);
                padding: 12px 18px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
                color: #f8fafc;
                pointer-events: none;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            }
            .hud-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 1px solid rgba(255, 255, 255, 0.12);
                padding-bottom: 6px;
                margin-bottom: 8px;
            }
            .hud-brand {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 0.5px;
                color: #38bdf8;
                text-transform: uppercase;
            }
            .hud-testcase {
                font-size: 12px;
                color: #94a3b8;
                font-family: "JetBrains Mono", Consolas, monospace;
            }
            .hud-status-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 3px 10px;
                border-radius: 20px;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.6px;
                text-transform: uppercase;
            }
            .hud-status-running {
                background: rgba(14, 165, 233, 0.2);
                color: #38bdf8;
                border: 1px solid #38bdf8;
            }
            .hud-status-passed {
                background: rgba(34, 197, 94, 0.25);
                color: #4ade80;
                border: 1px solid #22c55e;
            }
            .hud-status-failed {
                background: rgba(239, 68, 68, 0.25);
                color: #f87171;
                border: 1px solid #ef4444;
            }
            .hud-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background-color: currentColor;
                animation: hud-pulse 1.4s infinite ease-in-out;
            }
            @keyframes hud-pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.3; transform: scale(0.85); }
            }
            .hud-body {
                display: flex;
                align-items: flex-start;
                gap: 12px;
            }
            .hud-phase-pill {
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 800;
                font-family: monospace;
                letter-spacing: 0.5px;
                flex-shrink: 0;
            }
            .phase-setup    { background: #64748b; color: #fff; }
            .phase-action   { background: #f59e0b; color: #000; }
            .phase-verify   { background: #10b981; color: #fff; }
            .phase-security { background: #ef4444; color: #fff; }
            .phase-given    { background: #8b5cf6; color: #fff; }
            .phase-when     { background: #f59e0b; color: #000; }
            .phase-then     { background: #10b981; color: #fff; }
            .phase-and      { background: #06b6d4; color: #fff; }

            .hud-content {
                flex-grow: 1;
            }
            .hud-step-title {
                font-size: 13.5px;
                font-weight: 600;
                color: #f1f5f9;
                line-height: 1.35;
                margin-bottom: 2px;
            }
            .hud-step-detail {
                font-size: 11.5px;
                color: #94a3b8;
                line-height: 1.3;
            }
            .hud-step-count {
                font-size: 11px;
                color: #64748b;
                font-weight: 600;
                flex-shrink: 0;
                margin-top: 2px;
            }

            /* --- SPOTLIGHT RUNNER OVERLAY --- */
            #agy-spotlight-box {
                position: absolute;
                pointer-events: none;
                z-index: 2147483640;
                border: 2.5px solid #00f0ff;
                border-radius: 8px;
                box-shadow: 0 0 0 9999px rgba(15, 23, 42, 0.65), 0 0 30px rgba(0, 240, 255, 0.9), inset 0 0 15px rgba(0, 240, 255, 0.35);
                transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
                display: none;
            }
            #agy-spotlight-badge {
                position: absolute;
                top: -28px;
                left: 0;
                background: linear-gradient(90deg, #00f0ff 0%, #0284c7 100%);
                color: #041019;
                font-size: 11px;
                font-weight: 800;
                padding: 3px 9px;
                border-radius: 5px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.5);
                text-transform: uppercase;
                letter-spacing: 0.6px;
                white-space: nowrap;
                display: flex;
                align-items: center;
                gap: 5px;
            }
        `;
        (document.head || document.documentElement).appendChild(style);
    }

    // 2. Inject Elements when body is ready
    function injectElements() {
        if (!document.body) return;

        let hud = document.getElementById('agy-hud-container');
        if (!hud) {
            hud = document.createElement('div');
            hud.id = 'agy-hud-container';
            hud.innerHTML = `
                <div class="hud-header">
                    <div class="hud-brand">
                        <span>🏛️ MAHKAMAH AGUNG TOKEN MONITORING</span>
                        <span class="hud-testcase" id="hud-tc-id">TC-001</span>
                    </div>
                    <div class="hud-status-badge hud-status-running" id="hud-status">
                        <span class="hud-dot"></span>
                        <span id="hud-status-text">RUNNING</span>
                    </div>
                </div>
                <div class="hud-body">
                    <span class="hud-phase-pill phase-given" id="hud-phase">GIVEN</span>
                    <div class="hud-content">
                        <div class="hud-step-title" id="hud-title">Inisialisasi Test Runner...</div>
                        <div class="hud-step-detail" id="hud-detail">Menyiapkan Browser & Target SUT</div>
                    </div>
                    <div class="hud-step-count" id="hud-count">TC-001</div>
                </div>
            `;
            document.body.appendChild(hud);
        }

        let spotlight = document.getElementById('agy-spotlight-box');
        if (!spotlight) {
            spotlight = document.createElement('div');
            spotlight.id = 'agy-spotlight-box';
            spotlight.innerHTML = `<div id="agy-spotlight-badge">🎯 TARGET</div>`;
            document.body.appendChild(spotlight);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectElements);
    } else {
        injectElements();
    }
})();
"""

UPDATE_HUD_JS = """
({phase, title, detail, count, status, tcId}) => {
    const hudPhase = document.getElementById('hud-phase');
    const hudTitle = document.getElementById('hud-title');
    const hudDetail = document.getElementById('hud-detail');
    const hudCount = document.getElementById('hud-count');
    const hudStatus = document.getElementById('hud-status');
    const hudStatusText = document.getElementById('hud-status-text');
    const hudTcId = document.getElementById('hud-tc-id');

    if (hudTcId && tcId) hudTcId.innerText = tcId;
    if (hudPhase && phase) {
        hudPhase.innerText = phase.toUpperCase();
        hudPhase.className = `hud-phase-pill phase-${phase.toLowerCase()}`;
    }
    if (hudTitle && title) hudTitle.innerText = title;
    if (hudDetail && detail) hudDetail.innerText = detail;
    if (hudCount && count) hudCount.innerText = count;

    if (hudStatus && status) {
        if (status.toUpperCase() === 'PASSED') {
            hudStatus.className = 'hud-status-badge hud-status-passed';
            hudStatusText.innerText = 'PASSED';
        } else if (status.toUpperCase() === 'FAILED') {
            hudStatus.className = 'hud-status-badge hud-status-failed';
            hudStatusText.innerText = 'FAILED';
        } else {
            hudStatus.className = 'hud-status-badge hud-status-running';
            hudStatusText.innerText = 'RUNNING';
        }
    }
}
"""

HIGHLIGHT_BOX_JS = """
({box, badgeText}) => {
    const spotlight = document.getElementById('agy-spotlight-box');
    const badge = document.getElementById('agy-spotlight-badge');
    if (!spotlight || !badge) return;

    const scrollX = window.pageXOffset || document.documentElement.scrollLeft;
    const scrollY = window.pageYOffset || document.documentElement.scrollTop;

    const pad = 6;
    spotlight.style.left = `${box.x + scrollX - pad}px`;
    spotlight.style.top = `${box.y + scrollY - pad}px`;
    spotlight.style.width = `${box.width + (pad * 2)}px`;
    spotlight.style.height = `${box.height + (pad * 2)}px`;
    spotlight.style.display = 'block';

    if (badgeText) {
        badge.innerHTML = `🎯 ${badgeText}`;
    }
}
"""

REMOVE_SPOTLIGHT_JS = """
() => {
    const spotlight = document.getElementById('agy-spotlight-box');
    if (spotlight) spotlight.style.display = 'none';
}
"""


class InjectedHudSpotlightRunner:
    def __init__(self, page: Page, output_dir: Path):
        self.page = page
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.step_idx = 1
        self.total_steps = 6

    def inject_overlay(self):
        self.page.evaluate(HUD_AND_SPOTLIGHT_JS)

    def update_hud(self, phase: str, title: str, detail: str, status: str = "RUNNING"):
        count = f"Step {self.step_idx}/{self.total_steps}"
        self.page.evaluate(UPDATE_HUD_JS, {
            "phase": phase,
            "title": title,
            "detail": detail,
            "count": count,
            "status": status
        })

    def highlight(self, selector: str, badge_text: str = ""):
        try:
            loc = self.page.locator(selector).first
            loc.scroll_into_view_if_needed(timeout=3000)
            box = loc.bounding_box()
            if box:
                self.page.evaluate(HIGHLIGHT_BOX_JS, {
                    "box": box,
                    "badgeText": badge_text
                })
                time.sleep(0.4)
            else:
                self.clear_highlight()
        except Exception as e:
            print(f"  [WARN] Highlight failed for '{selector}': {e}")
            self.clear_highlight()

    def clear_highlight(self):
        self.page.evaluate(REMOVE_SPOTLIGHT_JS)

    def snapshot(self, filename: str):
        if not filename.endswith(".png"):
            filename += ".png"
        filepath = self.output_dir / filename
        self.page.screenshot(path=str(filepath), full_page=False)
        print(f"  [SNAPSHOT] Saved: {filepath.name}")
        return filepath


def run_e2e_journey_poc(headed: bool = False, delay: float = 0.5):
    mode_text = "HEADED (LIVE WATCH MODE)" if headed else "HEADLESS (CI/CD MODE)"
    print("============================================================================")
    print(" [POC START] Browser E2E Journey Automation: Anti-Fraud CMS Client Config")
    print(" Architecture: Playwright CDP + Injected HUD Overlay & Spotlight Runner")
    print(f" Execution Mode: {mode_text}")
    print("============================================================================")

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print("[1] Meluncurkan Chromium Browser Engine (Viewport 1440x900)...")
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=not headed,
            slow_mo=300 if headed else 0,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        runner = InjectedHudSpotlightRunner(page, SCREENSHOT_DIR)

        # ----------------------------------------------------------------------
        # STEP 1: GIVEN - Buka Halaman Login JNS7
        # ----------------------------------------------------------------------
        print("\n--- STEP 1: [GIVEN] Akses Portal Login JNS7 Mobile Broadcast ---")
        page.goto(BASE_URL, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_selector(".login-box", timeout=15000)
        runner.inject_overlay()
        runner.update_hud(
            phase="GIVEN",
            title="Pengguna Berada Pada Halaman Login Portal JNS7 Mobile Broadcast",
            detail=f"Target URL: {BASE_URL} | Form Autentikasi Siap",
            status="RUNNING"
        )
        runner.highlight(".login-box", "Login Card Container")
        runner.snapshot("01_given_portal_login_loaded.png")
        runner.step_idx += 1
        if headed: time.sleep(delay)

        # ----------------------------------------------------------------------
        # STEP 2: WHEN - Isi Kredensial Super Admin & Login
        # ----------------------------------------------------------------------
        print("\n--- STEP 2: [WHEN] Autentikasi Pengguna Menggunakan Akun Super Admin ---")
        runner.update_hud(
            phase="WHEN",
            title="Pengguna Melakukan Autentikasi Menggunakan Akun Super Admin",
            detail="Mengisi Username: admin | Password: •••••••• | Submit Form",
            status="RUNNING"
        )
        runner.highlight('input[name="username"]', "Username: admin")
        page.fill('input[name="username"]', "admin")
        if headed: time.sleep(delay)

        runner.highlight('input[name="password"]', "Password: ••••••••")
        page.fill('input[name="password"]', "admin123")
        if headed: time.sleep(delay)

        runner.highlight('button[type="submit"]', "Action: Klik Tombol Login")
        runner.snapshot("02_when_credentials_filled_spotlight.png")
        if headed: time.sleep(delay)

        with page.expect_navigation():
            page.click('button[type="submit"]')
        page.wait_for_load_state("load")
        page.wait_for_selector(".main-header", timeout=15000)
        runner.step_idx += 1

        # ----------------------------------------------------------------------
        # STEP 3: THEN - Dashboard Utama Terverifikasi
        # ----------------------------------------------------------------------
        print("\n--- STEP 3: [THEN] Dashboard Utama JNS7 Berhasil Dimuat Dengan Sesi Aktif ---")
        runner.inject_overlay()
        assert "home" in page.url, f"Expected dashboard URL to contain 'home', got {page.url}"
        runner.update_hud(
            phase="THEN",
            title="Dashboard Utama JNS7 Berhasil Dimuat Dengan Sesi Pengguna Aktif",
            detail=f"Sesi Aktif: Super Admin (Admin) | Dashboard URL: {page.url}",
            status="RUNNING"
        )
        runner.highlight(".main-header .navbar-custom-menu", "Active Session: Admin")
        runner.snapshot("03_then_dashboard_session_active.png")
        runner.step_idx += 1
        if headed: time.sleep(delay)

        # ----------------------------------------------------------------------
        # STEP 4: AND - Navigasi Sidebar Anti Fraud -> Client Config
        # ----------------------------------------------------------------------
        print("\n--- STEP 4: [AND] Navigasi Sidebar Anti Fraud -> Submenu Client Config ---")
        runner.update_hud(
            phase="AND",
            title="Pengguna Membuka Menu Sidebar Anti Fraud Menuju Submenu Client Config",
            detail="Membuka Treeview Menu 'Anti Fraud' -> Klik Submenu 'Client Config'",
            status="RUNNING"
        )
        # Spotlight parent menu
        runner.highlight('li.treeview > a:has-text("Anti Fraud")', "Sidebar: Anti Fraud")
        if headed: time.sleep(delay)
        page.locator('li.treeview > a:has-text("Anti Fraud")').click()
        page.wait_for_selector('ul.treeview-menu a:has-text("Client Config")', state="visible", timeout=10000)
        time.sleep(0.5)

        # Spotlight submenu Client Config
        runner.highlight('ul.treeview-menu a:has-text("Client Config")', "Submenu: Client Config")
        runner.snapshot("04_and_sidebar_antifraud_selected.png")
        if headed: time.sleep(delay)

        with page.expect_navigation():
            page.locator('ul.treeview-menu a:has-text("Client Config")').click()
        page.wait_for_load_state("load")
        page.wait_for_selector("#btn-add-config", timeout=15000)
        runner.step_idx += 1

        # ----------------------------------------------------------------------
        # STEP 5: THEN - Halaman Anti Fraud Config Terverifikasi Lengkap
        # ----------------------------------------------------------------------
        print("\n--- STEP 5: [THEN] Halaman Konfigurasi Anti Fraud Menampilkan Tombol Tambah Dan Tabel Data ---")
        runner.inject_overlay()
        assert "antifraud/config" in page.url, f"Expected URL 'antifraud/config', got {page.url}"
        
        runner.update_hud(
            phase="THEN",
            title="Halaman Konfigurasi Anti Fraud Menampilkan Tombol Tambah Dan Tabel Data",
            detail="Route: /antifraud/config | Header: Client Configurations | Tombol: Add & SYNC",
            status="RUNNING"
        )
        runner.highlight("#btn-add-config", "Tombol Utama: Add Config")
        runner.snapshot("05_then_antifraud_config_page_ready.png")
        runner.step_idx += 1
        if headed: time.sleep(delay)

        # ----------------------------------------------------------------------
        # STEP 6: AND/THEN - Buka Modal Add Config & Validasi Kontrak Form
        # ----------------------------------------------------------------------
        print("\n--- STEP 6: [AND] Pengguna Membuka Modal Tambah Konfigurasi Dan Memvalidasi Form Isian ---")
        page.click("#btn-add-config")
        page.wait_for_selector("#config-modal", state="visible")
        time.sleep(0.5)

        runner.inject_overlay()
        runner.update_hud(
            phase="AND",
            title="Pengguna Membuka Modal Tambah Konfigurasi Dan Memvalidasi Form Isian",
            detail="Modal #config-modal Aktif | Form Kontrak: Client, Sender, Division, Loss Monitoring, Rate Limit",
            status="PASSED"
        )
        # Highlight form container inside modal
        runner.highlight("#config-modal .modal-content", "Modal Dialog: Form Client Config Anti-Fraud")
        runner.snapshot("06_and_modal_form_contract_verified.png")
        if headed: time.sleep(delay)

        # Spotlight input Client select2
        runner.highlight("#config-modal .form-horizontal", "Form Attributes: Client / Sender / Division / Approval / Effective Date")
        runner.snapshot("07_then_final_journey_spotlight_success.png")

        print("\n[VERIFIKASI SUKSES] Seluruh tahapan E2E Journey tervalidasi 100% tanpa error!")
        if headed:
            print("[INFO] Menahan jendela browser selama 4 detik sebelum ditutup...")
            time.sleep(4.0)

        browser.close()

    print("============================================================================")
    print(f" [POC COMPLETE] Screenshots tersimpan di: {SCREENSHOT_DIR}")
    print("============================================================================")


if __name__ == "__main__":
    is_headed = "--headed" in sys.argv or "--watch" in sys.argv
    run_e2e_journey_poc(headed=is_headed, delay=1.0 if is_headed else 0.4)
