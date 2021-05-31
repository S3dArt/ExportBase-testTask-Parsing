import requests
from bs4 import BeautifulSoup as bs
import time
import threading
import json

urls = [
    'https://www.rusprofile.ru/codes/89220',
    'https://www.rusprofile.ru/codes/429110'
]



headers = {'accept': '*/*', 'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.'
    '36'}


def parse(base_url, headers, company_names, company_info, company_status):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        # Получаем количество страниц
        res_peging = soup.find_all('div', class_='search-result-paging')
        urls = [base_url]

        for page in res_peging:
            page_url = page.find('a').get('href')
            urls.append('https://www.rusprofile.ru/' + page_url)

        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            # Парсим названием компании
            parse_company_names(soup, company_names)

            #  Парсим инфу о компании(всё в одной строчке)
            parse_company_info(soup, company_info)

            # парсим статус компании(у некоторых есть)
            parse_company_status(soup, company_status)
    else:
        print('ERROR')


def parse_company_names(soup, company_names):
    temp_names = []
    divs = soup.find_all('div', class_="company-item__title")
    for div in divs:
        links = div.select('a')  # читать примечание после кода
        name = links[0].text if links else ''  # если в div этого типа может быть только одна ссылка
        # (если их больше - остальные проигнорируются)
        # name = ', '.join([link.text for link in links]) # если в div этого типа может быть несколько ссылок,

        temp_names.append(name.split('\n')[0].strip())  # сплитим по переносу строки и выбираем только
        # первый элемент в котором название компании, во втором элементе откуда-то появляется пустая строка
        # удаляем все пробелы перед названием
    return company_names.extend(temp_names)


def parse_company_info(soup, company_info):
    divs = soup.find_all('div', class_="company-item-info")
    info_list = []
    for div in divs:
        links = div.select('dd')
        info_list.append([link.text for link in links])
        #info = ', '.join([link.text for link in links])  # вся информация о компании

        # Не у всех есть капитал
        i = 0
        for info in info_list[1::3]:
            if len(info) == 3:
                if len(info[0]) == 13:
                    info_list[1::3][i].insert(0, 'None')

                else:
                    info_list[1::3][i].append('None')
            i += 1

    return company_info.extend(info_list[1::3])  # срез по требуемой информации


def parse_company_status(soup, company_status):
    divs = soup.find_all('div', class_="company-item")
    status_list = []
    for div in divs:
        links = div.select('span')
        status = links[0].text if links else 'None'
        status_list.append(status)
    return company_status.extend(status_list)



company_names = []
company_info = []
company_status = []

# start = time.time()
# for url in urls:
#     parse(url, headers, company_names, company_info, company_status)
# print(f'Sequential: {time.time() - start : .2f} seconds')
#
# print()


start = time.time()
threads = []
for url in urls:
    thread = threading.Thread(target=parse, args=(url, headers, company_names, company_info, company_status))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

#print(f'Threading: {time.time() - start : .2f} seconds')

print(company_names)
print(company_info)
print(company_status)


# data_dict = []
# count = 0
# for item in range(len(company_names)):
#     data = {
#         'company_name': company_names[item],
#         'company_ogrn': company_info[item][1],
#         'company_inn' : company_info[item][0],
#         'company_status': company_status[item],
#         'company_registration_date': company_info[item][2],
#         'company_capital': company_info[item][3]
#     }
#     count += 1
#     print(f'#{count}: company is done')
#     data_dict.append(data)
#
#     with open('data2.json', 'w') as json_file:
#         json.dump(data_dict, json_file, indent=4)