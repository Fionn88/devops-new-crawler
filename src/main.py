from bs4 import BeautifulSoup
import requests
import config
import datetime

header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
today = datetime.date.today() - datetime.timedelta(days=1)

def crawl(page, if_daliy) -> list:

    # 須解決有些 News 沒有 Tag，導致無法判斷是12篇中的 News 是哪一篇沒有
    data = []
    url = f"https://devops.com/category/news/?_page={page}"
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser') 
    all_subjects = soup.find_all('h4', class_ = 'pt-cv-title')
    all_tags = soup.find_all('span', class_ = 'terms')
    all_times = soup.find_all('span', class_ = 'entry-date')
    all_authors = soup.find_all('span', class_ = 'author')
    original_format = " %B %d, %Y"

    if if_daliy == True:
        for index in range(12):
            parsed_date = datetime.datetime.strptime(all_times[index].text, original_format)
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            compare_date = formatted_date.split('-')
            if datetime.datetime(today.year, today.month, today.day) <= datetime.datetime(int(compare_date[0]), int(compare_date[1]), int(compare_date[2])):
                data.append([all_subjects[index].text, all_tags[index].text, formatted_date, all_authors[index].text])
            else:
                break
        return data
    else:
        for index in range(12):
            if page == 3:
                print(all_tags[index].text)
            parsed_date = datetime.datetime.strptime(all_times[index].text, original_format)
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            compare_date = formatted_date.split('-')
            data.append([all_subjects[index].text, all_tags[index].text, formatted_date, all_authors[index].text])
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