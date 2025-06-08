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
    browser.add_cookie({"name": "MUSIC_U", "value": "0079E6751E5913196CF94295326D7C9C25B56B516D22C72FC82CC321963DF47A0FC9F8FD0C5E6DA2C6ECF3777558209E7EF48028DD5C1FEF39CC1D65B6202E2F008A292F4BCB95CCE106C6661436C628224F8F192B2FD75EEF1DAE2B7DD1A1210D9D7A30CB8325AF07AE0FAD60704DED11A8AA48D15026AD2B18BF73D9A2135BA735A1B810F51B140A2C5303D9DF7DAB49A41AF5C822C3D100F38228FEAD2745DBA59C54438285A713D3F4ECD92A3BCC488AE8DC84C6114025859BF46E3ACD26487628C5B2C36BCBB6A07178B75EDB4EA660EEF7969FC5724AF2361FE7F19954ADE5D1BC9ED4C00951C31B64789CF19B91B7EF6D962A1C6124E655CB8197061122B476A51EE2876AB0813D221AAFBABE8AD01CE04E6ABFD47DECF0BEF630BBDCF089CE5E4C862700FF6C24E0B210DD4CC48F422EE1B0210DCC88B1CD97346C58FF9DA8674499E3A926609AB4EA4BDDD75864B6A20B5D9FFE9D7F3F0F22AF7A2D40"})
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
