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
job_offers = website_json['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['groupedOffers']
with open("dane.json", "w") as data:
    data.write(json.dumps(job_offers, indent=1))
with open("dane.json", "r") as data:
    job_offers = json.load(data)
for job in range(len(job_offers)):
    cos = job_offers[job]
    print(cos)
    print(f"Tytuł: {cos['jobTitle']}")
    print(f"Widełki płacowe: {cos['salaryDisplayText']}")
    print("LOKALIZACJA:")
    if not cos['isRemoteWorkAllowed']:
        for offer in range(len(cos['offers'])):
            for city in cos['offers'][offer]['displayWorkplace'].replace(" ","").split(","):
                print(city)
            print(len(cos['offers']))
    else: print("zdalna")
    print("TECHNOLOGIE:", "nie podano" if len(cos['technologies']) == 0 else "")
    for technology in range(len(cos['technologies'])):
        print(cos['technologies'][technology])
    print("POZYCJE:")
    print(cos['positionLevels'])
    for position in range(len(cos['positionLevels'])):
        print(cos['positionLevels'][position])
    print()
