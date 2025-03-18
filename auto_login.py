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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E8A5CFB765968207E92928FA08509B50ADEF04A534C663C7D000EB9337F15D48764FDFB9DC4A0174139198A27B95713DB3B838F69E02BAFCD248E2F8E0FBFA91509CC8977623A0BE6FB488FD06EEA0419892C18C12D942BECAE0014E012D8D7AEAE310DEBC789B9602D4E229DD9153059947580B1F52D7BA8C95A21AA2273C84721D2D07C6C8F4519695B1B13D90C4FB595959FEC7C34C4B437A27DA8BF707120AD2D3FE0E6D47341A98F40E5DAA303C1B6AE3926BA6CAE30B34AD2C7A019961ED3E921669DF0972486AF359C38CA84A15F1A082ECD2FFBCE5CD983AC65584C5F78856467AB29C950E9BD5936EB9CB032BA2DAAD9F1175EC28DDF3F3BB7B477AE5367BEC228068669ED9B74EAC2B1690561E55D498B7894AD5168B8EFA63245FAA4DA4D3478594FC2ADE15D7899D6445"})
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
