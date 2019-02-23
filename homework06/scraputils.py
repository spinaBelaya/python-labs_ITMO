import requests
from bs4 import BeautifulSoup
import time


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    table = parser.find("table", attrs={"class": "itemlist"})
    tr_list = table.find_all("tr")
    print(len(tr_list) - 2)
    info_tr = [[tr_list[i], tr_list[i + 1]] for i in range(0, len(tr_list) - 2, 3)]
    i = 0

    for news in info_tr:
        a_com = news[1].find_all("a")[-1]


        if a_com.text == "discuss" or a_com.text == 'hide':
            comment = "No comments"
        else:
            comment = int(a_com.text.split("\xa0")[0])
        if news[1].find("a", attrs={"class": "hnuser"}) != None:
            author = news[1].find("a", attrs={"class": "hnuser"}).text
        else:
            author = 'hidden'
        if news[1].find("span", attrs={"class": "score"}) != None:
            likes = int(news[1].find("span", attrs={"class": "score"}).text.split()[0])
        else:
            likes = 0

        info_dict = {
            'title': news[0].find("a", attrs={"class": "storylink"}).text,
            'author': author,
            'points': likes,
            'url': news[0].find("a", attrs={"class": "storylink"})['href'],
            'comments': comment
        }
        news_list.append(info_dict)
        i += 1

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    table = parser.find("table", attrs={"class": "itemlist"})
    print( table.find_all("a")[-1].text)
    if table.find_all("a")[-1].text == "More":
        link = parser.find("a", attrs={"class": "morelink"})['href']
        print(link)
    else:
        link = ''

    return link


def get_news(url="https://news.ycombinator.com/newest?next=19195692&n=931", n_pages=3):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1

    return news



