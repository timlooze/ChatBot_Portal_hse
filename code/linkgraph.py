from tokenize_data import tokenize_data
from textparser import Header, Paragraph

"""
Function for searching down the structure of the graph of links to tokenize all the information
"""


def get_on_depth(header, n, tokenize_flg=False):
    if n == 1 or type(header) == Paragraph or len(header.objects) == 0:
        res = header.__str__()
        if tokenize_flg:
            res = tokenize_data(res)
        for i in range(n - 1):
            res = [res]
        return res
    else:
        objects = []
        for o in header.objects:
            objects.append(get_on_depth(o, n - 1, tokenize_flg))
        return objects


"""
Get_text allows us to convert html web classes to the text and save it
"""


def get_text(link):
    import requests as rq
    from bs4 import BeautifulSoup
    from textparser import parse
    # Code takes the link of the site to parse
    r = rq.get(link)
    web = BeautifulSoup(r.text, 'html.parser')
    # Deciding which class to parse
    if link == 'https://portal.hse.ru':
        soup = web.findAll('div', {'class': 'splash_preview__descr'})
    elif web.find('div', {'class': 'post__text'}) is None:
        return []
    elif len(web.find('div', {'class': 'post__text'}).find_all('div',
                                                               {"class": "with-indent5 _builder builder--text"})) == 0:
        soup = web.findAll('div', {'class': 'post__text'})
    else:
        soup = web.find('div', {'class': 'post__text'}).findAll('div',
                                                                {"class": "with-indent5 _builder builder--text"})
    # Filtering convert text
    soup = list(filter(lambda x: len(x.text) > 10, soup))
    if len(soup) == 0:
        return ""
    page = [parse(soup[i], link) for i in range(len(soup))]
    if len(page) == 1:
        return page[0]
    new_page = Header(page[0].header_text)
    new_page.objects = page
    return new_page


"""
Class LinkGraph saves the structure of our site link and allows us to switch between neighbour links
"""


class LinkGraph:
    def __init__(self):
        from tqdm import tqdm
        self.matrix = {}
        print('go_get_links')
        self.bs4_test('https://portal.hse.ru')
        self.link_text = {}
        for i in tqdm(self.matrix.keys()):
            self.link_text[i] = get_text(i)
        print(self.matrix['https://portal.hse.ru'])

    # Deletes rubbish tags like /en and others
    def bs4_test(self, url):
        import requests
        from bs4 import BeautifulSoup
        color_mass = set()

        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        for link in soup.find_all('a'):
            try:
                if 'portal.hse' in link.get('href') and '/en' not in link.get('href'):  # англ не нужен
                    curr_link = link.get('href')
                    if '#' in curr_link:
                        curr_link = curr_link[:curr_link.find('#')]  # убираю якорные ссылки - по сути дубли
                    if '?' in curr_link:
                        curr_link = curr_link[:curr_link.find('?')]
                    if curr_link[4] != 's':
                        curr_link = curr_link[:4] + 's' + curr_link[4:]
                    curr_link = curr_link.strip('/')
                    color_mass.add(curr_link)
            finally:
                continue
        self.matrix[url] = color_mass
        for link in color_mass:
            if link not in self.matrix.keys():
                self.bs4_test(link)
    # Returns lists of links on web-sites and text of them
    def get_link_text(self):
        sentences = []
        links = []
        for k, v in self.link_text.items():
            if type(v) != list:
                sentences.append(v)
                links.append(k)
        return links, sentences
