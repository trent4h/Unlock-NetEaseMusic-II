# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0052E144089FD1AB1495D27FE6B55B477DFD7A70664FDC200624D3C997A046893EB968C97EA8FC75D7677B2547266229C5C05A6B6A5FA493D15407B8DE55458215CB3197AA4890E1C2C7A82C2E7AE901C689BAC5894F3BC99B10EB2AC20EBA354A59BC6264739D32B001006D78C1C8A2C047901AAD0D5AA867132030A619644979CB7D409AC9FB8FB93192BD0E6ABBE3F47FE1C421280D0CECDCCD42934D61FED1FE966A59AC334290C3A30BE18A06B42514C5A1C9C2C47B543EEFD1FF4F5644890A09A812252F9C496F6AEBD7A13BEF7E311D9018AE130D908878E9CE132F62FFF57BB12D8201ED3D74674B5526B93C8DB5B981E11C337019AF4E1360321F7961ED20CD25C49FBDB58F986B304E0480D9E0A7820202F42C71B2B1090073C11CEE659747CAD87A9B4ED2B7C72BC71746F3FBC38E6E42CB3C49E00CB4451B1E1F09E844C4A894AD6D4E32BF09334F4544E2E73A318ECAF8B83ACA4689937E2E9E2E"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
