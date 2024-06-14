from bs4 import BeautifulSoup
import requests
import config
import datetime

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple\
          WebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
today = datetime.date.today() - datetime.timedelta(days=1)


def crawl(page, if_daliy) -> list:

    data = []
    url = f"https://devops.com/category/news/?_page={page}"
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')
    all_subjects = soup.find_all('h4', class_='pt-cv-title')
    all_things = soup.find_all('div', class_='pt-cv-meta-fields')
    original_format = "%B %d, %Y"

    if if_daliy:
        for index in range(12):
            all_things_list = all_things[index].text.split(' | ')
            if len(all_things_list) < 3:
                tags = ""
            else:
                tags = all_things_list[2]
            entry_time = all_things_list[1]
            author = all_things_list[0]
            parsed_date = datetime.datetime.\
                strptime(entry_time, original_format)
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            compare_date = formatted_date.split('-')
            if datetime.datetime(today.year, today.month, today.day) <= \
               datetime.datetime(
                    int(compare_date[0]),
                    int(compare_date[1]),
                    int(compare_date[2])
                    ):
                data.append(
                    [all_subjects[index].text, tags, formatted_date, author]
                    )
            else:
                break
        return data
    else:
        for index in range(12):
            all_things_list = all_things[index].text.split(' | ')
            if len(all_things_list) < 3:
                tags = ""
            else:
                tags = all_things_list[2]
            entry_time = all_things_list[1]
            author = all_things_list[0]
            parsed_date = datetime.datetime.\
                strptime(entry_time, original_format)
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            data.append(
                [all_subjects[index].text, tags, formatted_date, author]
                )
        return data


def first_crawl():
    # init db

    # crawl the 6 months data
    result = []
    for page in range(1, 12):
        result.extend(crawl(page, False))
    print(result)


def daliy_crawl():
    result = crawl(1, True)
    # return data to db
    print(result)


if __name__ == "__main__":
    if config.FIRST_CRAWL == "True":
        first_crawl()
    else:
        daliy_crawl()
