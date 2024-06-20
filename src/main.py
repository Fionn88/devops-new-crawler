from bs4 import BeautifulSoup
import requests
import config
import datetime
import database
import logging

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple\
          WebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}


def crawl(page, if_daliy) -> list:

    data = []
    url = f"https://devops.com/category/news/?_page={page}"
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')
    all_subjects = soup.find_all('h4', class_='pt-cv-title')
    all_things = soup.find_all('div', class_='pt-cv-meta-fields')
    original_format = "%B %d, %Y"
    if_loop = False

    for index in range(12):
        all_things_list = all_things[index].text.split(' | ')
        if len(all_things_list) < 3:
            tags = ""
        else:
            tags = all_things_list[2]
        entry_time = all_things_list[1]
        author = all_things_list[0]
        link = all_subjects[index].find('a')['href']
        parsed_date = datetime.datetime.\
            strptime(entry_time, original_format)
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        compare_date = formatted_date.split('-')
        if if_daliy:
            today = datetime.date.today() - datetime.timedelta(days=1)
            if datetime.datetime(today.year, today.month, today.day) <= \
               datetime.datetime(
                    int(compare_date[0]),
                    int(compare_date[1]),
                    int(compare_date[2])
                    ):
                id = link[link[:-1].rfind('/')+1:-1]
                data.append(
                    [id, all_subjects[index].text, tags,
                     formatted_date, author, link]
                    )
            else:
                return data, if_loop
        else:
            today = datetime.date.today() - datetime.timedelta(days=180)
            if datetime.datetime(today.year, today.month, today.day) <= \
               datetime.datetime(
                    int(compare_date[0]),
                    int(compare_date[1]),
                    int(compare_date[2])
                    ):
                id = link[link[:-1].rfind('/')+1:-1]
                data.append(
                    [id, all_subjects[index].text, tags,
                     formatted_date, author, link]
                    )
            else:
                return data, if_loop
    if_loop = True
    return data, if_loop


def scrape_last_six_months_articles():

    database.create_tables()
    result = []
    page = 1
    if_loop = True
    while if_loop:
        data_list, if_loop = crawl(page, False)
        result.extend(data_list)
        page += 1
    database.insert_data(result)


def scrape_last_two_days_articles():
    result = []
    page = 1
    if_loop = True
    while if_loop:
        data_list, if_loop = crawl(page, True)
        result.extend(data_list)
        page += 1
    if result:
        database.insert_data(result)
    else:
        logging.info("There's no data available for the past two days.")


if __name__ == "__main__":
    if config.FIRST_CRAWL == "True":
        scrape_last_six_months_articles()
    else:
        scrape_last_two_days_articles()
