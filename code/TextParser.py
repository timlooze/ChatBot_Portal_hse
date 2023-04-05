
# %%
import requests as rq
from bs4 import BeautifulSoup


# %%


class Header:
    def __init__(self, header_text):
        self.name = 'h'
        self.header_text = header_text
        self.objects = []

    def __str__(self):
        result = f'**{self.header_text}**\n'
        for i in self.objects:
            result += f'{str(i)}\n'
        return result

    def str_with_out_atrifacts(self):
        result = f'{self.header_text}\n'
        for i in self.objects:
            result += f'{i.str_with_out_atrifacts()}\n'
        return result

    def append(self, o):
        self.objects.append(o)

    def get_pairs(self):
        result = []
        for i in self.objects:
            if i.name == 'h':
                result += i.get_pairs()
            else:
                result.append((self.header_text, str(i)))
        if len(result) > 0 and len(result[-1]) != 2:
            print(i, result[-1])
        return result


# %%
class Image:
    def __init__(self, tag):
        self.alt = tag.get('alt')
        self.src = tag.get('src')


# %%
class Paragraph:
    def __init__(self, tag, not_recursive_paragraph=True):
        self.name = tag.name
        self.paragraph_text = tag.text
        self.paragraph_text_with_artifacts = tag.text
        self.images = []
        for i in tag.find_all(True, recurcive=False):
            if i.name == 'strong' and not_recursive_paragraph and i.text != '':
                self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace(
                    i.text, f' **{i.text}** ')
            elif i.name == 'a' and not_recursive_paragraph and i.text != '':
                self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace(
                    i.text, f'[{i.text}]({i.get("href")})')
            elif i.name == 'em' and not_recursive_paragraph and i.text != '':
                self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace(
                    i.text, f' __{i.text}__ ')
            elif i.name == 'img':
                self.images.append(Image(i))
            elif i.name in ('p', 'div', 'li', 'ul'):
                recurcive = Paragraph(i, False)
                self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace(
                    recurcive.paragraph_text_with_artifacts, recurcive.paragraph_text)
                self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace(
                    recurcive.paragraph_text, recurcive.paragraph_text_with_artifacts)
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('  ', ' ')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('  ', ' ')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('  ', ' ')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('  ', ' ')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('** **', '')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('** **', '')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('** **', '')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('** **', '')

    def __str__(self):
        return self.paragraph_text_with_artifacts

    def str_with_out_atrifacts(self):
        return self.paragraph_text


# %%
def parse(soup, text):
    current_h1 = Header(text)
    current_h2 = None
    current_h3 = None
    current_h4 = None
    for tag in soup.find_all(True, recursive=False):
        if current_h4:
            current_header = current_h4
        elif current_h3:
            current_header = current_h3
        elif current_h2:
            current_header = current_h2
        else:
            current_header = current_h1
        if tag.name == 'h2':
            current_h2 = Header(tag.text)
            current_h1.append(current_h2)
            current_h3 = None
            current_h4 = None
        elif tag.name == 'h3':
            current_h3 = Header(tag.text)
            if current_h2:
                current_h2.append(current_h3)
            else:
                current_h1.append(current_h3)
            current_h4 = None
        elif tag.name == 'h4':
            current_h4 = Header(tag.text)
            if current_h3:
                current_h3.append(current_h4)
            elif current_h2:
                current_h2.append(current_h4)
            else:
                current_h1.append(current_h4)

        elif tag.name in ('p', 'div', 'ul', 'ol'):
            current_header.append(Paragraph(tag))
    return current_h1


# %%
r = rq.get('https://portal.hse.ru/personalpages')
web = BeautifulSoup(r.text, 'html.parser')
soup = web.find('div', {"class": "post__text"})
personalpages = parse(soup, 'Персональные страницы')
# %%
r = rq.get('https://portal.hse.ru/helpsite')
web = BeautifulSoup(r.text, 'html.parser')
soup = web.find('div', {"class": "post__text"})
helpsite = parse(soup, 'Как осуществляется доступ к редактированию сайта на портале?')
# %%
r = rq.get('https://portal.hse.ru/progs')
web = BeautifulSoup(r.text, 'html.parser')
soup = web.find('div', {'class': 'post__text'}).find('div', {"class": "with-indent5 _builder builder--text"})
progs = parse(soup, 'Инструкция по редактированию нового сайта образовательной программы')
# %%
r = rq.get('https://portal.hse.ru/poll')
web = BeautifulSoup(r.text, 'html.parser')
soup = web.find('div', {'class': 'post__text'}).find_all('div', {"class": "with-indent5 _builder builder--text"})[1:]
poll = Header('Регистрационная форма / опрос')
for i in soup:
    temp = parse(i, 'Регистрационная форма / опрос')
    poll.objects += temp.objects
# %%
r = rq.get('https://portal.hse.ru/im')
web = BeautifulSoup(r.text, 'html.parser')
soup = web.find('div', {'class': 'post__text'}).find_all('div', {"class": "with-indent5 _builder builder--text"})
im = Header('Создание и редактирование сайта подразделения')
for i in soup:
    temp = parse(i, 'Создание и редактирование сайта подразделения')
    im.objects += temp.objects
# %%
# headers = [personalpages, helpsite, progs, poll, im]
# for i in headers:
#     for name, value in i.get_pairs():
#         print(name)
#         print(value)
#         print()
#     print()