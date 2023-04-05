"""
Илья автоматизируй эту функцию
"""



def get_text(link):
    import requests as rq
    from bs4 import BeautifulSoup
    from TextParser import parse
    r = rq.get(link)
    web = BeautifulSoup(r.text, 'html.parser')
    if link == 'https://portal.hse.ru':
        soup = web.findAll('div', {'class': 'splash_preview__descr'})
        return [parse(soup[i], link) for i in range(len(soup))]
    if web.find('div', {'class': 'post__text'}) is None:
        return []
    if len(web.find('div', {'class': 'post__text'}).find_all('div', {"class": "with-indent5 _builder builder--text"})) == 0:
        soup = web.findAll('div', {'class': 'post__text'})
    else:
        soup = web.find('div', {'class': 'post__text'}).findAll('div',
                                                         {"class": "with-indent5 _builder builder--text"})
    soup = list(filter(lambda x: len(x.text) > 300, soup))
    if len(soup) == 0:
        return ""
    return [parse(soup[i], link) for i in range(len(soup))]


class LinkGraph:
    def __init__(self):
        from tqdm import tqdm
        self.matrix = {}
        self.bs4_test('https://portal.hse.ru')
        self.link_text = {}
        print(self.matrix.keys())
        for i in tqdm(self.matrix.keys()):
            self.link_text[i] = get_text(i)
            if len(self.link_text[i]) == 0:
                del self.link_text[i]

    def bs4_test(self, url):
        import requests
        from bs4 import BeautifulSoup
        color_mass = set()

        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        for link in soup.find_all('a'):
            try:
                if 'https://portal.hse' in link.get('href') and '/en' not in link.get('href'): # англ не нужен
                    curr_link = link.get('href')
                    if '#' in curr_link:
                        curr_link = curr_link[:curr_link.find('#')] # убираю якорные ссылки - по сути дубли
                    if '?' in curr_link:
                        curr_link = curr_link[:curr_link.find('?')]
                    curr_link = curr_link.strip('/')
                    color_mass.add(curr_link)
            finally:
                continue
        self.matrix[url] = color_mass
        for link in color_mass:
            if link not in self.matrix.keys():
                self.bs4_test(link)

    def get_link_text(self):
        return self.link_text


import json
a = LinkGraph()
b = a.get_link_text()
print(b)
print(len(b))

# %%
import json
b = {1 : 1}
try:
    with open('result.json', 'w') as fp:
        json.dump(b, fp)
finally:
    print("Ooops")