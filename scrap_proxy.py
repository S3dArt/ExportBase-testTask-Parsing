import requests
import random
from bs4 import BeautifulSoup as bs
import time

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # получаем ответ HTTP и создаем объект soup
    soup = bs(requests.get(url).content, "lxml")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies


free_proxies = get_free_proxies()

# print(f'Обнаружено бесплатных прокси - {len(free_proxies)}:')
# for i in range(len(free_proxies)):
#     print(f"{i+1}) {free_proxies[i]}")

def get_session(proxies):
    # Создать HTTP - сеанс
    session = requests.Session()
    # выбираем один случайный прокси
    proxy = random.choice(proxies)
    session.proxies = {'http': 'http://' + proxy, "https": 'https://' + proxy}
    return session



# proxy_work = ['128.199.214.87:3128', '161.202.226.194:80', '169.57.1.84:8123', '34.203.142.175:80', '119.81.189.194:80', '198.50.163.192:3129', '78.47.16.54:80', '175.143.37.162:80', '176.235.182.99:8080', '216.21.18.193:80', '41.59.90.92:80', '68.183.241.131:80', '185.235.41.85:80', '180.250.170.210:59778', '183.88.226.50:8080', '186.125.59.8:46316', '92.204.129.161:80', '213.230.97.10:3128', '82.99.217.18:8080', '169.57.1.85:80', '51.222.21.94:32768', '160.16.144.198:3128', '178.128.143.54:8080', '103.138.172.65:80', '46.99.185.140:8080', '103.28.121.58:80', '181.13.209.35:8080', '45.130.229.230:443', '185.169.198.98:3128', '61.7.146.7:8082', '64.227.122.38:8080', '23.251.138.105:8080', '51.222.21.93:32768', '103.138.172.66:80', '51.222.21.92:32768', '190.64.18.177:80', '136.233.122.204:80', '219.95.129.8:80', '49.156.45.169:8080', '46.175.70.69:44239', '182.253.170.163:8080', '192.99.239.215:8080', '36.89.18.217:8080', '87.237.234.187:3128', '103.240.77.98:30093', '88.247.10.31:8080', '213.230.91.75:3128', '113.190.243.229:80', '103.138.172.67:80', '136.243.211.104:80', '95.217.251.149:3128', '102.68.129.30:8080', '212.174.61.18:8080', '103.83.116.202:55443', '13.36.102.214:80', '221.120.210.211:39617', '194.106.175.218:8080', '195.177.217.45:80', '3.123.122.80:80', '95.141.36.112:8686', '118.174.196.112:36314', '84.54.82.173:3128', '104.40.153.131:80']
# for i in range(100):
#     s = get_session(proxy_work)
#     try:
#         print("Страница запроса с IP:", s.get("http://icanhazip.com", timeout=2).text.strip())
#     except Exception as e:
#         print(e)
#         continue
#

# worked_proxy = []
# for i in range(300):
#     try:
#         r = requests.get('http://httpbin.org/ip', proxies={'http': 'http://' + free_proxies[i], 'https': 'https://' + free_proxies[i]}, timeout=2)
#         print(r.json())
#         worked_proxy.append(free_proxies[i])
#     except:
#         print('fail')
#         pass

