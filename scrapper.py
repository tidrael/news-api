import json
from datetime import datetime
import requests

import models
from database import SessionLocal, engine
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=ChromeService(executable_path=ChromeDriverManager().install()),
    chrome_options=chrome_options,
)

path = "web-scrapper.json"

db = SessionLocal()
today = datetime.today().strftime("%Y-%m-%d")


def get_news(path):
    scrapper_list = json.loads(open(path).read())
    for content in scrapper_list:
        url = content["url"]
        xpath = content["xpath"]
        driver.get(url)
        article = driver.find_elements(By.XPATH, xpath)
        for element in article:
            db_news = models.News(title=element.text, day=today)
            db.add(db_news)
            db.commit()
