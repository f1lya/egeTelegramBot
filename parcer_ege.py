import requests
import time
from bs4 import BeautifulSoup

urls = ["https://math-ege.sdamgia.ru", "https://rus-ege.sdamgia.ru",
        "https://en-ege.sdamgia.ru", "https://de-ege.sdamgia.ru", "https://fr-ege.sdamgia.ru",
        "https://sp-ege.sdamgia.ru", "https://phys-ege.sdamgia.ru", "https://chem-ege.sdamgia.ru",
        "https://bio-ege.sdamgia.ru", "https://geo-ege.sdamgia.ru", "https://soc-ege.sdamgia.ru",
        "https://lit-ege.sdamgia.ru", "https://hist-ege.sdamgia.ru", "https://inf-ege.sdamgia.ru"]
hrefs = []

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
        hrefs.append('/test?id=' + str(a) + '&print=true&pdf=h')
    print(hrefs)


def get_file(href):
    r = requests.get(href, stream=True)
    return r


def save_doc(name, file_obj):
    with open(name, 'bw') as f:
        for chunk in file_obj.iter_content(8192):
            f.write(chunk)


def main():
    for url in urls:
        get_links(get_html(url))
        for href, num in zip(hrefs, number):
            href = url + href
            name = href.partition('-ege.sdamgia.ru/test?id=')[0]
            name = name.split('//')[1] + " 2019-09-" + num + ".pdf"
            save_doc(name, get_file(href))
            print(name)
        time.sleep(3)


if __name__ == '__main__':
    main()
