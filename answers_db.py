import requests
import pymysql
from bs4 import BeautifulSoup
import time
import datetime


connection = pymysql.connect(host='localhost', user='root', password='gs651zv3mlt8@#GHCZ', db='ege_bot', charset='utf8mb4')
cursor = connection.cursor()
print("SUCCESSFULLY CONNECTED")

urls = ["https://mathb-ege.sdamgia.ru", "https://math-ege.sdamgia.ru", "https://rus-ege.sdamgia.ru",
        "https://en-ege.sdamgia.ru", "https://de-ege.sdamgia.ru", "https://fr-ege.sdamgia.ru",
        "https://sp-ege.sdamgia.ru", "https://phys-ege.sdamgia.ru", "https://chem-ege.sdamgia.ru",
        "https://bio-ege.sdamgia.ru", "https://geo-ege.sdamgia.ru", "https://soc-ege.sdamgia.ru",
        "https://lit-ege.sdamgia.ru", "https://hist-ege.sdamgia.ru", "https://inf-ege.sdamgia.ru"]

hrefs = []
answer = []

number = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15",
          "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]


def get_html(url):
    r = requests.get(url)
    return r.text


def get_links(html):
    hrefs.clear()
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='new_header').find('table').find('tr', class_='pinkmark')
    a = divs.find('td')
    a = a.find('a').get('href')
    a = a.split('=')[1]
    count = 0
    while count < 31:
        count += 1
        a = int(a) + 1
        hrefs.append('/test?id=' + str(a) + '&print=true')


def get_answer(html):
    answer.clear()
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', 'answer')
    for div in divs:
        span = div.find('span').text.split('Ответ: ')[1]
        if '|' in span:
            span = span.split('|')[0]
        answer.append(span)
    while len(answer) < 30:
        answer.append("None")


def main():
    for url in urls:
        get_links(get_html(url))
        for href, num in zip(hrefs, number):
            href = url + href
            name = href.partition('-ege.sdamgia.ru/test?id=')[0]
            exam = name.split('//')[1]
            numberTest = str("2019-09-" + num)
            get_answer(get_html(href))
            cursor.execute("""
                            INSERT INTO answers (exam, numberTest, ans_1, ans_2, ans_3, ans_4, ans_5, ans_6, 
                            ans_7, ans_8, ans_9, ans_10, ans_11, ans_12, ans_13, ans_14, ans_15, ans_16,
                            ans_17, ans_18, ans_19, ans_20, ans_21, ans_22, ans_23, ans_24, ans_25, ans_26,
                            ans_27, ans_28, ans_29, ans_30)
                            VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (exam, numberTest, answer[0],
                            answer[1], answer[2], answer[3], answer[4], answer[5], answer[6], answer[7], answer[8],
                            answer[9], answer[10], answer[11], answer[12], answer[13], answer[14], answer[15],
                            answer[16], answer[17], answer[18], answer[19], answer[20], answer[21], answer[22],
                            answer[23], answer[24], answer[25], answer[26], answer[27], answer[28], answer[29]))
            connection.commit()
        time.sleep(3)


if __name__ == '__main__':
    main()

