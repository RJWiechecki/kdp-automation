#!/usr/local/bin/python3

# =====================================
# Kindle Direct Publishing Auto Scraper
# Full Production Refactor (April 2025)
# =====================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
from pathlib import Path
import time

# === Configuration ===
FIREFOX_PROFILE = "/Users/admin/Dev/KDPAutomation/browser_profiles/FirefoxUserDataClean"
DOWNLOADS = str(Path.home() / "Downloads")
COOKIES_FILE = "cookies.pkl"
TARGET_URL = "https://kdpreports.amazon.com/dashboard"
DOWNLOAD_BUTTON_XPATH = "//button[contains(., 'Download report')]"

# === Launch Browser ===
def launch_browser():
    print("\U0001F680 Launching Firefox with trusted profile...")
    options = Options()
    options.add_argument("--no-remote")
    options.add_argument(f"-profile")
    options.add_argument(FIREFOX_PROFILE)
    options.set_preference("signon.autologin.proxy", True)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", DOWNLOADS)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    options.set_preference("browser.download.useDownloadDir", True)
    options.set_preference("pdfjs.disabled", True)
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    return driver

# === Navigate and Download ===
def navigate_and_download(driver):
    print("\U0001F449 Navigating to KDP Reports page...")
    driver.get(TARGET_URL)

    # Close any tabs that aren't kdpreports
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        
        if "kdpreports.amazon.com" in driver.current_url:
            print(f"✅ Found KDP Dashboard tab: {driver.current_url}")
            break
        else:
                print(f"❌ Closing unwanted tab: {driver.current_url}")
                driver.close()

    # Switch focus back to KDP if necessary
    driver.switch_to.window(driver.window_handles[0])

    # === Load cookies (safe injection only) ===
    added_count = 0
    skipped_count = 0

    if os.path.exists(COOKIES_FILE):
        print("\U0001F4D1 Loading cookies from file...")
        with open(COOKIES_FILE, "rb") as f:
            cookies = pickle.load(f)
        current_domain = driver.current_url.split("/")[2]  # kdpreports.amazon.com

        for cookie in cookies:
            domain = cookie.get("domain")
            if "kdpreports.amazon.com" in domain or "kdp.amazon.com" in domain:
                try:
                    driver.add_cookie(cookie)
                    added_count += 1
                except Exception:
                    print(f"⚠️ Skipping invalid cookie: {cookie.get('name', 'unknown')} ({domain})")
            else:
                skipped_count += 1

        driver.refresh()
        print(f"✅ {added_count} cookies injected successfully, {skipped_count} skipped.")
        time.sleep(5)

    # === Double-check for login ===
    if "signin" in driver.current_url.lower():
        print("\U0001F6AB No valid cookies. Manual login required!")
        input("Login manually (OTP if needed), then press ENTER to continue...")
        with open(COOKIES_FILE, "wb") as f:
            pickle.dump(driver.get_cookies(), f)
        print("✅ Cookies updated after manual login.")

    # === Wait for download button ===
    print("⏳ Waiting for 'Download report' button to appear...")
    try:
        wait = WebDriverWait(driver, 30)
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, DOWNLOAD_BUTTON_XPATH)))

        print("\U0001F44B Clicking Download Report button...")
        download_button.click()
        print(f"✅ Download triggered. Check {DOWNLOADS} folder!")

    except Exception as e:
        print(f"\U0001F6AB Error: {e}")

# === Main Runner ===
def run_scraper():
    driver = launch_browser()
    try:
        navigate_and_download(driver)
    finally:
        input("\nPress ENTER to close browser...")
        driver.quit()

if __name__ == "__main__":
    run_scraper()

