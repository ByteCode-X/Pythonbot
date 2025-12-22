import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config import SESSION_ID, GC_URL
from utils import log_lifecycle


# =========================
# BROWSER SETUP
# =========================

def launch_browser():
    log_lifecycle("Browser launch started")

    chrome_options = Options()

    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)

    # Open Instagram first (required before setting cookies)
    driver.get("https://www.instagram.com/")
    time.sleep(5)

    # Inject session cookie
    driver.add_cookie({
        "name": "sessionid",
        "value": SESSION_ID,
        "domain": ".instagram.com",
        "path": "/",
        "secure": True,
        "httpOnly": True
    })

    # Reload to activate login
    driver.refresh()
    time.sleep(6)

    log_lifecycle("Session restored via cookie")

    return driver


def open_group_chat(driver):
    log_lifecycle("Opening group chat")

    driver.get(GC_URL)
    time.sleep(8)

    # Focus page by clicking body (prevents input bugs)
    try:
        driver.find_element(By.TAG_NAME, "body").click()
    except Exception:
        pass

    log_lifecycle("Group chat opened")
