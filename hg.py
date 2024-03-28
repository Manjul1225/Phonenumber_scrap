from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import *
from time import sleep
import urllib.parse
import json
from unidecode import unidecode
from datetime import datetime

def Find_Elements(driver : webdriver.Chrome, by, value : str) -> list[WebElement]:
    while True:
        try:
            elements = driver.find_elements(by, value)
            if len(elements) > 0:
                break
        except:
            pass
        sleep(0.1)
    return elements

service = Service(executable_path="E:\Work\hungary_phone_scrap\chromedriver-win64\chromedriver.exe")   
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9030")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.130 Safari/537.36")
driver = webdriver.Chrome(service=service, options=options)

for character in ["X", "Y", "Z"]:
    search_input = driver.find_element(By.ID, 'residential-search-term-input-header')
    search_input.clear()
    search_input.send_keys(character)
    search_button = driver.find_element(By.ID, 'btn-search-header')
    driver.execute_script("arguments[0].click();", search_button)
    sleep(1)
    text = driver.find_element(By.CLASS_NAME, 'search-results-count-data-residential').text
    totals = int(text.split('of ')[1].split(' ')[0])
    print(f"There are {totals} cities and phones in {character}")
    count = 0
    while True:
        result = []
        for i in range(20):
            boxes = Find_Elements(driver, By.CLASS_NAME, 'residential-customer')
            contents = boxes[i].find_elements(By.CLASS_NAME, 'detail-text')
            city_name = contents[0].text.split(' ')[-1]
            try:
                driver.execute_script("arguments[0].click();", contents[1])
                alert = driver.switch_to.alert
                alert.accept()
                driver.switch_to.default_content()
            except:
                pass
            boxes = Find_Elements(driver, By.CLASS_NAME, 'residential-customer')
            phone_number = boxes[i].text.split('\n')[3]
            count += 1
            print(f"{count}({totals}).", city_name, phone_number)
            result.append({"city" : city_name, "phone" : phone_number})
            if count == totals:
                break
        with open(f"result/{character}_{count-19}_{count}.json", 'w') as file:
            json.dump(result, file) 
        try:
            next_page = driver.find_element(By.CLASS_NAME, 'pagination').find_elements(By.TAG_NAME, 'li')[-1].find_element(By.TAG_NAME, 'a')
            driver.execute_script("arguments[0].click();", next_page)
        except:
            break
        sleep(1)