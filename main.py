import json
from selenium import webdriver
from math import ceil
from bs4 import BeautifulSoup
from math import floor

website_link = 'https://it.pracuj.pl/praca?et=17%2C4%2C18&sal=1&sc=0&wm=home-office%2Cfull-office%2Chybrid'
chrome_driver = webdriver.Chrome()
chrome_driver.get(website_link)
website_soup = BeautifulSoup(chrome_driver.page_source, "html.parser")
website_script = website_soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"}).text
chrome_driver.quit()
website_json = json.loads(website_script)
job_offers = website_json['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['groupedOffers']
jobs_found_amount = website_json['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['groupedOffersTotalCount']
pages = ceil(jobs_found_amount / 50)
page_number = 2
with open("dane.json", "w") as data:
    data.write(json.dumps(job_offers, indent=1))
with open("dane.json", "r") as data:
    job_offers = json.load(data)
for job in range(len(job_offers)):
    the_job = job_offers[job]
    print(the_job)
    print(f"Tytuł: {the_job['jobTitle']}")
    salary_display_text = the_job["salaryDisplayText"]
    salary_string = salary_display_text.replace("\xa0", "").replace(" ", "")
    salary_range = salary_string.split("zł")
    if len(salary_range[0].split("–")) == 1:
        min_max_pay = [salary_range[0].split("–")[0], salary_range[0].split("–")[0]]
    else:
        min_max_pay = [salary_range[0].split("–")[0], salary_range[0].split("–")[1]]
    if "godz" in salary_string:
        min_max_pay[0] = floor(float(min_max_pay[0]) * 173.3)
        min_max_pay[1] = floor(float(min_max_pay[1]) * 173.3)
    print(f"Widełki płacowe: {min_max_pay[0]}-{min_max_pay[1]}zł")
    print("LOKALIZACJA:")
    if not the_job['isRemoteWorkAllowed']:
        for offer in range(len(the_job['offers'])):
            for city in the_job['offers'][offer]['displayWorkplace'].replace(" ", "").split(","):
                print(city)
            print(len(the_job['offers']))
    else:
        print("zdalna")
    print("TECHNOLOGIE:", "nie podano" if len(the_job['technologies']) == 0 else "")
    for technology in range(len(the_job['technologies'])):
        print(the_job['technologies'][technology])
    print("POZYCJE:")
    for position in range(len(the_job['positionLevels'])):
        print(the_job['positionLevels'][position])
    print()
