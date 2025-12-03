import json
from selenium import webdriver
from bs4 import BeautifulSoup
from math import floor


def connection():
    website_link = f'https://it.pracuj.pl/praca?et=17,4,18,&sal=1&pn=1&sc=0&wm=home-office,full-office,hybrid'
    chrome_driver = webdriver.Chrome()
    chrome_driver.get(website_link)
    website_soup = BeautifulSoup(chrome_driver.page_source, "html.parser")
    website_script = website_soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"}).text
    chrome_driver.quit()
    website_json = json.loads(website_script)
    page_job_offers = website_json['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['groupedOffers']
    page_jobs_found_amount = website_json['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['groupedOffersTotalCount']
    return page_job_offers, page_jobs_found_amount


def save_and_load_job_data():
    my_connection = connection()
    with open("dane.json", "w") as data:
        data.write(json.dumps(my_connection[0], indent=1))
    with open("dane.json", "r") as data:
        return json.load(data), my_connection[1]


def convert_hourly_salary_to_monthly(hourly_salary):
    return floor(float(hourly_salary) * 173.3)


def prepare_salary_range(salary_text):
    salary_string = salary_text.replace("\xa0", "").replace(" ", "").replace(",", ".")
    salary_range = salary_string.split("zł")
    if len(salary_range[0].split("–")) == 1:
        min_max_pay = [salary_range[0].split("–")[0], salary_range[0].split("–")[0]]
    else:
        min_max_pay = [salary_range[0].split("–")[0], salary_range[0].split("–")[1]]
    if "godz" in salary_string:
        min_max_pay[0] = convert_hourly_salary_to_monthly(min_max_pay[0])
        min_max_pay[1] = convert_hourly_salary_to_monthly(min_max_pay[1])
    return min_max_pay


def print_multiple_workplaces(offers_list):
    for offer in range(len(offers_list)):
        city_list = offers_list[offer]['displayWorkplace'].replace(" ", "").split(",")
        for city in city_list:
            print(city)


def print_data_to_console(jobs_list):
    for job in range(len(jobs_list)):
        the_job = jobs_list[job]
        print(the_job)
        print(f"Tytuł: {the_job['jobTitle']}")
        job_salary = prepare_salary_range(the_job["salaryDisplayText"])
        print(f"Widełki płacowe: {job_salary[0]}-{job_salary[1]}zł")
        print("LOKALIZACJA:")
        if not the_job['isRemoteWorkAllowed']:
            print_multiple_workplaces(the_job['offers'])
        else:
            print("zdalna")
        print("TECHNOLOGIE:", "nie podano" if len(the_job['technologies']) == 0 else "")
        for technology in range(len(the_job['technologies'])):
            print(the_job['technologies'][technology])
        print("POZYCJE:")
        for position in range(len(the_job['positionLevels'])):
            print(the_job['positionLevels'][position])
        print()


current_save = save_and_load_job_data()
job_offers = current_save[0]
jobs_found_amount = current_save[1]
print_data_to_console(job_offers)
print(jobs_found_amount)
