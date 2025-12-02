import json
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

website_link = 'https://it.pracuj.pl/praca?et=17%2C4%2C18&sal=1&sc=0&wm=home-office%2Cfull-office%2Chybrid'
chrome_driver = webdriver.Chrome()
chrome_driver.get(website_link)
website_soup = BeautifulSoup(chrome_driver.page_source, "html.parser")
website_script = website_soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"}).text
chrome_driver.quit()
website_json = json.loads(website_script)
print(website_json['props']['pageProps']['dehydratedState']['queries'][0]['state']['data'])
