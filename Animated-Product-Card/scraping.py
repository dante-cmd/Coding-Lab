from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException, WebDriverException
from selenium.webdriver.support.ui import Select, WebDriverWait  # available since 2.4.0

from pathlib import Path
from urllib.parse import urljoin
from lxml.html import fromstring
import time
import json

from pymongo import MongoClient
from pathlib import Path
import json
        


if not Path('adidas.html').exists():
    
    driver_path = r'C:\dmozilla\geckodriver.exe'
    ser = Service(driver_path)
    opt = webdriver.FirefoxOptions()
    
    # don't show the browser
    # opt.add_argument('-headless')

    # Create a new instance of the Chrome driver
    driver = webdriver.Firefox(service=ser, options=opt)

    # go to the Adidas website
    driver.get("https://www.adidas.com/us/shoes?grid=true")
    
    # wait for the page to load
    SCROLL_PAUSE_TIME = 3
    new_height = 0
    START = 0

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom 500px by 500px
        driver.execute_script(f"window.scrollTo({START}, {START + 500});")
        START += 500

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height +=500
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height >= last_height:
            break

    try:
        page = driver.page_source
        with open('adidas.html', 'w') as f:
            json.dump(page, f)
            
            print('Downloading adidas.html')
            time.sleep(5)
            print('Downloading adidas.html completed, closing driver')
            driver.quit()
    except Exception as e:
        print(e)
        driver.quit()
else :
    with open('adidas.html', 'r') as f:
        page = json.load(f)
        dataImg = []
        
        tree = fromstring(page)
        imgs = tree.xpath('//div[@class="glass-product-card__assets"]//a/img')
        for i, img in enumerate(imgs):
            if img.attrib['src']:
                if img.attrib['src'].endswith('.jpg'):
                    dataImg.append({img.attrib['src'].split('/')[-1] : img.attrib['src']})
                
        # save to MongoDB
        try:
            mongo_uri = "mongodb://localhost"
            client = MongoClient(mongo_uri)

            db = client['adidas']
            collection = db['datapage']
            collection.insert_many(dataImg)
            print('Inserted to MongoDB')
        except Exception as e:
            print(e)
            
           