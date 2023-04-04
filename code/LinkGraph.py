"""
Илья автоматизируй эту функцию
"""
def get_text(link):
    import requests as rq
    from bs4 import BeautifulSoup
    from TextParser import parse
    r = rq.get(link)
    web = BeautifulSoup(r.text, 'html.parser')
    soup = web.find('div', {'class': 'post__text'}).find('div',
                                                         {"class": "with-indent5 _builder builder--text"})
    return parse(soup, link)


class LinkGraph:
    def __init__(self):
        from tqdm import tqdm
        self.matrix = {}
        self.bs4_test('https://portal.hse.ru')
        self.link_text = {}
        print(self.matrix.keys())
        for i in tqdm(self.matrix.keys()):
            self.link_text[i] = get_text(i)

    def bs4_test(self, url):
        import requests
        from bs4 import BeautifulSoup
        color_mass = set()

        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        for link in soup.find_all('a'):
            try:
                if 'portal.hse' in link.get('href'):
                    color_mass.add(link.get('href'))
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
b = a.get_link_text
print(b)

# %%
import json
b = {1 : 1}
try:
    with open('result.json', 'w') as fp:
        json.dump(b, fp)
finally:
    print("Ooops")