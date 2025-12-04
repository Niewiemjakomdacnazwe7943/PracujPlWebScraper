import json
from selenium import webdriver
from bs4 import BeautifulSoup
from math import floor, ceil

programming_languages = {
    ".net": 0,
    "angular": 0,
    "aws": 0,
    "c++": 0,
    "C#": 0,
    "-C": 0,
    "Go": 0,
    "hibernate": 0,
    "html": 0,
    "javascript": 0,
    "java": 0,
    "node.js": 0,
    "python": 0,
    "php": 0,
    "react": 0,
    "ruby": 0,
    "rust": 0,
    "-R": 0,
    "sql": 0,
    "typescript": 0
}
work_modes = {
    "Młodszy specjalista (Junior)": 0,
    "Specjalista (Mid / Regular)": 0,
    "Starszy specjalista (Senior)": 0
}


def first_connection():
    current_save = connection(1)
    first_job_offers = current_save[0]
    first_job_offers_amount = current_save[1]
    with open("dane.json", "w") as data:
        data.write("")
    return first_job_offers, first_job_offers_amount


def find_pages_amount(amount_of_offers):
    return ceil(amount_of_offers / 50)


def connection(page_number):
    website_link = f'https://it.pracuj.pl/praca?et=17,4,18,&sal=1&pn={page_number}&sc=0&wm=home-office,full-office,hybrid'
    chrome_driver = webdriver.Chrome()
    chrome_driver.get(website_link)
    website_soup = BeautifulSoup(chrome_driver.page_source, "html.parser")
    website_script = website_soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"}).text
    chrome_driver.quit()
    website_json = json.loads(website_script)
    page_job_offers = website_json['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['groupedOffers']
    jobs_found_amount = website_json['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['groupedOffersTotalCount']
    return page_job_offers, jobs_found_amount


def save_and_load_job_data(all_job_data):
    with open("dane.json", "w") as data:
        data.write(json.dumps(all_job_data, indent=1))
    with open("dane.json", "r") as data:
        return json.load(data)


def convert_hourly_salary_to_monthly(hourly_salary):
    return floor(float(hourly_salary) * 173.3)


def prepare_salary_range(salary_text):
    salary_string = salary_text.replace("\xa0", "").replace(" ", "").replace(",", ".")
    salary_range = salary_string.split("zł")
    if len(salary_range[0].split("–")) == 1:
        min_max_pay = [int(salary_range[0].split("–")[0])]
        if "godz" in salary_string:
            min_max_pay[0] = int(convert_hourly_salary_to_monthly(min_max_pay[0]))
    else:
        min_max_pay = [int(salary_range[0].split("–")[0]), int(salary_range[0].split("–")[1])]
        if "godz" in salary_string:
            min_max_pay[0] = convert_hourly_salary_to_monthly(min_max_pay[0])
            min_max_pay[1] = convert_hourly_salary_to_monthly(min_max_pay[1])
    return min_max_pay


def print_multiple_workplaces(offers_list):
    for offer in range(len(offers_list)):
        city_list = offers_list[offer]['displayWorkplace'].replace(" ", "").split(",")
        for city in city_list:
            print(city)


def format_programming_languages(keys, values):
    new_languages = {}
    for j in range(len(keys)):
        if len(keys[j].split("-")) == 2:
            keys[j] = keys[j].split("-")[1]
    for k in range(len(keys)):
        new_languages[keys[k]] = values[k]
    return new_languages


def print_data_to_console(jobs_list):
    for job_offer in range(len(jobs_list)):
        the_job = jobs_list[job_offer]
        print(the_job)
        print(f"Tytuł: {the_job['jobTitle']}")
        job_salary = prepare_salary_range(the_job["salaryDisplayText"])
        print(f"Widełki płacowe: {job_salary[0]}-{job_salary[1]}zł" if len(job_salary) == 2 else f"Płaca: {job_salary[0]}zł")
        print("LOKALIZACJA:")
        if not the_job['isRemoteWorkAllowed']:
            print_multiple_workplaces(the_job['offers'])
        else:
            print("zdalna")
        print("TECHNOLOGIE:", "nie podano" if len(the_job['technologies']) == 0 else "")
        for technology in range(len(the_job['technologies'])):
            print(the_job['technologies'][technology])
        print("POZYCJE:")
        for pos in range(len(the_job['positionLevels'])):
            print(the_job['positionLevels'][pos])
        print()


job_data = first_connection()
job_offers = job_data[0]
job_offers_amount = job_data[1]
# print_data_to_console(job_offers)
pages_found = find_pages_amount(job_offers_amount)
for i in range(2, pages_found + 1):
    more_job_offers = connection(i)
    for job in more_job_offers[0]:
        job_offers.append(job)
all_job_offers = save_and_load_job_data(job_offers)
for job in all_job_offers:
    for tech in job['technologies']:
        for language in programming_languages:
            if language in f"{tech.lower() if len(tech) > 2 else f'-{tech}'}":
                programming_languages[language] += 1
                break
    for position in job['positionLevels']:
        if position != "Ekspert" and position != "Asystent":
            work_modes[position] += 1
formatted_languages = format_programming_languages(list(programming_languages.keys()),list(programming_languages.values()))
