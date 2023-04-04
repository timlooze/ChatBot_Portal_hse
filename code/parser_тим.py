def urlib_test():
    import urllib.request
    response = urllib.request.urlopen('https://portal.hse.ru')
    html = response.read()
    print(html)

matrix = {}
color_mass = set

def bs4_test():
    import requests
    from bs4 import BeautifulSoup

    url = 'https://portal.hse.ru'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    for link in soup.find_all('a'):
        print(link.get('href'))

bs4_test()