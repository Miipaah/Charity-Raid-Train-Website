from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

from dotenv import load_dotenv
import os

def get_fw_profit():

    load_dotenv() 
    
    fw_user = os.getenv('FOURTHWALL_PROXY_USER')
    fw_pass = os.getenv('FOURTHWALL_PROXY_PASS')


    #path to the ChromeDriver executable
    chrome_driver_path = r'C:\Users\Mihir Patel\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

    service = Service(chrome_driver_path)

    #configure options for broswer loading
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-software-rasterizer') 
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('--blink-settings=imagesEnabled=false') 
    options.add_argument('--disable-gpu') 
    options.add_argument('--log-level=99')

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920,1080)
    driver.get('https://charityraidtrain-shop.fourthwall.com/admin/dashboard/analytics/report/profit?precision=DAY&range=last90days')

    driver.find_element(By.NAME, 'username').send_keys(fw_user) 
    driver.find_element(By.NAME, 'password').send_keys(fw_pass)  # 
    sign_in_button = driver.find_element(By.XPATH, "//button[text()='Sign in']")
    sign_in_button.click()
    
    def element_text_matches_pattern(driver):
        element = driver.find_element(By.CSS_SELECTOR, 'h5[data-testid="Heading"]')
        text = element.text
        if re.match(r'\$\d+(\.\d{2})?', text):
            return element
        else:
            return None
    wait = WebDriverWait(driver, 10)
    matching_element = wait.until(element_text_matches_pattern)
    profit = (float(matching_element.text[1:]))
    driver.close()

    return profit
    # Close the browser when you're done

