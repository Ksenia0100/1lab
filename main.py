# Import libraries
import re
import urllib.parse

import requests
from bs4 import BeautifulSoup
#также надо поставить lxml
# pip install lxml

inputUrl = ''
endUrl = ''
lang = ''


# получение статуса кода от страницы
def status_code(url):
    page_response = requests.get(url)
    return page_response.status_code


# нахождение используемого языка при вводе ссылок
def find_lang(url: str):
    start = url.find('//') + 2
    end = url.find('.')
    language = url[start:end]
    return language


# проверка введеных страниц на доступность
def check_link():
    url = input()
    print('\n')
    error_code = status_code(url)
    while (error_code == 404):
        url = input('Enter a valid url:\n')
        error_code = status_code(url)
    return url


# настройка отбора страниц для проверок
def internal_not_special(href):
    if href:
        if re.compile('^/wiki/').search(href):
            if not re.compile(':').search(href):
                if not re.compile('#').search(href):
                    return True
    return False


# используется алгоритм поиска в глубину
def dfs(link: str, depth: int) -> bool:
    if depth < 7:
        # Достает ссылки с сайта
        nextPage = requests.get(link)
        page = BeautifulSoup(nextPage.text, 'lxml')
        mainBody = page.find(id="mw-content-text")
        links = mainBody.find_all('a', href=internal_not_special)
        # Итерация
        # for _ in range(depth):
        #     print("  ", end='')
        # print(f"{depth}: {link}")
        for url in links:
            # преобразование ссылки
            url_get = ("https://" + lang + ".wikipedia.org" + urllib.parse.unquote(url.get('href')))
            print(url_get)
            if url_get == endUrl:
                print('-' * 10)
                print("Found in " + str(depth) + " jumps")
                print(f"Found: {depth}: {link}")
                print('-' * 10)
                return True
            else:
                if dfs(url_get, depth + 1):
                    print('-' * 10)
                    print(f"Found: {depth}: {link}")
                    print('-' * 10)
                    return True
        return False
    # если глубина больше 6
    else:
        return False


if __name__ == '__main__':
    print('Введите начальную ссылку для поиска:')
    inputUrl = urllib.parse.unquote(check_link())
    # inputUrl = 'https://en.wikipedia.org/wiki/Action_fiction'
    print('Введите конечную ссылку для поиска:')
    endUrl = urllib.parse.unquote(check_link())
    # endUrl = 'https://en.wikipedia.org/wiki/Harry_S._Truman'
    if find_lang(inputUrl) == find_lang(endUrl):
        lang = find_lang(inputUrl)
        print("\nStart\n")
        if dfs(inputUrl, 1):
            print('-' * 10)
            print("Found ")
        else:
            print('-' * 10)
            print("Not found ")
        print('-' * 10)
    else:
        print('The language is wrong')
