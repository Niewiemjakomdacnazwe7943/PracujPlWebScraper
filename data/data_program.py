import json
from selenium import webdriver
from bs4 import BeautifulSoup
from math import floor, ceil


def load_gathering_data():
    with open("data/gathering_data.json", "r", encoding="UTF-8") as my_data:
        gathering_data = json.load(my_data)
        return gathering_data


def export_analysis_data(data_to_export):
    with open("data/analysis_data.json", "w", encoding="UTF-8") as my_data:
        my_data.write(json.dumps(data_to_export, indent=1))


def first_connection(ai_ml_link=False):
    current_save = connection(1, ai_ml_link)
    first_job_offers = current_save[0]
    first_job_offers_amount = current_save[1]
    return first_job_offers, first_job_offers_amount


def find_pages_amount(amount_of_offers):
    return ceil(amount_of_offers / 50)


def connection(page_number, ai_ml_link=False):
    ai_parameter = ""
    if ai_ml_link:
        ai_parameter = "&its=ai-ml"
    website_link = f'https://it.pracuj.pl/praca?et=4,17,18,&sal=1&pn={page_number}&sc=0&wm=home-office,full-office,hybrid{ai_parameter}'
    chrome_driver = webdriver.Chrome()
    chrome_driver.get(website_link)
    try:
        website_soup = BeautifulSoup(chrome_driver.page_source, "html.parser")
        website_script = website_soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"}).text
        chrome_driver.quit()
    except Exception as e:
        print(chrome_driver.page_source)
        print(e)
        exit(1)
    website_json = json.loads(website_script)
    page_job_offers = website_json['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['groupedOffers']
    jobs_found_amount = website_json['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['groupedOffersTotalCount']
    return page_job_offers, jobs_found_amount


def save_and_load_job_data(all_job_data):
    with open("data/job_data.json", "w", encoding="UTF-8") as data:
        data.write(json.dumps(all_job_data, indent=1))
    with open("data/job_data.json", "r") as data:
        return json.load(data)


def save_and_load_job_titles(title_list):
    with open("data/job_titles.txt", "w", encoding="UTF-8") as job_titles:
        job_titles.write(f"{title_list}")
    with open("data/job_titles.txt", "r", encoding="UTF-8") as job_titles:
        return job_titles.readlines()


def translate_job_title(title_to_translate):
    fixed_title = title_to_translate.replace("dveloper", "developer").replace("inż.", "inżynier")
    prepared_title = fixed_title.lower().replace("\n", "").replace("/", " ")
    keywords_list = prepared_title.split(" ")
    counter = 0
    for keyword in keywords_list:
        for position_2 in positions:
            if keyword == position_2:
                keywords_list[counter] = positions[position_2]['translation']
                break
            elif keywords_list[counter] == "data" and keywords_list[counter + 1] == "scientist":
                positions['data scientist']['count'] += 1
        counter += 1
    new_title = ""
    for keyword in keywords_list:
        new_title += f"{keyword}\n"
    return new_title


def convert_hourly_salary_to_monthly(hourly_salary):
    return floor(float(hourly_salary) * 173.3)


def prepare_salary_range(salary_text):
    salary_string = salary_text.replace("\xa0", "").replace(" ", "").replace(",", ".")
    salary_range = salary_string.split("zł")
    if len(salary_range[0].split("–")) == 1:
        if "godz" in salary_string:
            min_max_pay = [convert_hourly_salary_to_monthly(salary_range[0])]
        else:
            min_max_pay = [int(salary_range[0].split("–")[0])]
    else:
        if "godz" in salary_string:
            min_max_pay = [convert_hourly_salary_to_monthly(salary_range[0].split("–")[0]), convert_hourly_salary_to_monthly(salary_range[0].split("–")[1])]
        else:
            min_max_pay = [int(salary_range[0].split("–")[0]), int(salary_range[0].split("–")[1])]
    return min_max_pay


def print_multiple_workplaces(offers_list):
    for offer in range(len(offers_list)):
        city_list = offers_list[offer]['displayWorkplace'].replace(" ", "").split(",")
        for city in city_list:
            print(city)


def calculate_average_salary(salary_range):
    if len(salary_range) == 1:
        return salary_range[0]
    average_salary = float((salary_range[0] + salary_range[1]) / 2)
    return average_salary


def detect_programming_language(your_language_dict, technology_string, lang):
    if lang in f"{technology_string.lower() if len(technology_string) > 2 else f'-{technology_string}'}":
        your_language_dict[lang] += 1
        return True
    else:
        return False


def calculate_average_position_salary(position_and_salary_dict):
    average_salary_dict = {}
    for pos in position_and_salary_dict:
        average_salary_dict[pos] = round((position_and_salary_dict[pos]['salary sum'] / position_and_salary_dict[pos]['count']))
    return average_salary_dict


def format_programming_languages(keys, values):
    new_languages = {}
    for j in range(len(keys)):
        if len(keys[j].split("-")) == 2:
            keys[j] = keys[j].split("-")[1]
    for k in range(len(keys)):
        new_languages[keys[k]] = values[k]
    return new_languages


def find_ai_related_jobs():
    custom_connection = first_connection(True)
    ai_offers_amount = custom_connection[1]
    ai_offers = custom_connection[0]
    ai_offers_pages = find_pages_amount(ai_offers_amount)
    for j in range(2, ai_offers_pages + 1):
        more_ai_offers = connection(j, True)
        for ai_job in more_ai_offers[0]:
            ai_offers.append(ai_job)
    return ai_offers


def print_data_to_console(jobs_list):
    for job_offer in range(len(jobs_list)):
        the_job = jobs_list[job_offer]
        print(the_job)
        print(f"Tytuł: {the_job['jobTitle']}")
        salary = prepare_salary_range(the_job["salaryDisplayText"])
        print(f"Widełki płacowe: {salary[0]}-{salary[1]}zł" if len(salary) == 2 else f"Płaca: {salary[0]}zł")
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


data_to_gather = load_gathering_data()
programming_languages = data_to_gather['programming languages']
work_modes = data_to_gather['work modes']
positions = data_to_gather['positions']
positions_and_salaries = data_to_gather['positions and salaries']

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
job_titles_string = ""
ai_related_jobs_amount = find_ai_related_jobs()

for job in all_job_offers:
    job_title = job['jobTitle']
    for tech in job['technologies']:
        for language in programming_languages:
            if detect_programming_language(programming_languages, tech, language):
                break

    for work_mode in job['workModes']:
        work_modes[work_mode] += 1

    pay_range = prepare_salary_range(job['salaryDisplayText'])
    for position in job['positionLevels']:
        if position != "Ekspert" and position != "Asystent":
            prepared_position = position.replace(" ", "").split("(")[1].replace(")", "")
            positions_and_salaries[prepared_position]['count'] += 1
            positions_and_salaries[prepared_position]['salary sum'] += calculate_average_salary(pay_range)
    job_titles_string += f"{job['jobTitle']}\n"

all_job_titles = save_and_load_job_titles(job_titles_string)
average_salaries_per_position = calculate_average_position_salary(positions_and_salaries)
all_translated_job_titles = []

formatted_languages = format_programming_languages(list(programming_languages.keys()), list(programming_languages.values()))

for title in all_job_titles:
    all_translated_job_titles.append(translate_job_title(title))

for translated_title in all_translated_job_titles:
    position_found = False
    split_title = translated_title.split("\n")
    for title_fragment in split_title:
        for position in positions:
            if title_fragment == positions[position]['translation']:
                positions[position]['count'] += 1
                position_found = True
                break
    if not position_found:
        positions['pozostałe']['count'] += 1
ai_jobs_percentage = float(f"{len(ai_related_jobs_amount) / job_offers_amount * 100:.2f}")
work_modes_sum = 0

for work_mode in work_modes:
    work_modes_sum += work_modes[work_mode]

export_analysis_data([formatted_languages,work_modes,positions,ai_jobs_percentage, average_salaries_per_position])
