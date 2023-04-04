class LinkGraph:
    def __init__(self):
        self.matrix = {}
        self.bs4_test('https://portal.hse.ru')

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
