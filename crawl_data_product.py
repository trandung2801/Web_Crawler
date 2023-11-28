from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = 'https://cellphones.com.vn/mobile.html'
    driver.get(url)

    elems = driver.find_elements(By.CLASS_NAME,"product-info [href]")
    links =[elem.get_attribute('href') for elem in elems]
    print(links)
    len(links)