import nltk
from nltk import word_tokenize, SnowballStemmer
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
STOP_WORDS = stopwords.words("russian")
print(STOP_WORDS)

class Header:
    def __init__(self, header_text):
        self.name = 'h'
        self.header_text = header_text.replace('\\xa', ' ').replace('\\t', ' ').replace('\\n', ' ')
        self.objects = []

    def __str__(self):
        result = f'**{self.header_text}**\n'
        for i in self.objects:
            result += f'{str(i)}\n'
        return result

    def str_with_out_artifacts(self):
        result = f'{self.header_text}\n'
        for i in self.objects:
            result += f'{i.str_with_out_artifacts()}\n'
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
        return result


class Paragraph:
    def __init__(self, tag, not_recursive_paragraph=True):
        self.name = tag.name
        self.paragraph_text = tag.text.replace('\\xa', ' ').replace('\\t', ' ').replace('\\n', ' ')
        self.paragraph_text_with_artifacts = tag.text.replace('\\xa', ' ').replace('\\t', ' ').replace('\\n', ' ')
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
            elif i.name in ('p', 'div', 'li', 'ul'):
                recursive = Paragraph(i, False)
                self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace(
                    recursive.paragraph_text_with_artifacts, recursive.paragraph_text)
                self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace(
                    recursive.paragraph_text, recursive.paragraph_text_with_artifacts)
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('  ', ' ')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('  ', ' ')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('  ', ' ')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('  ', ' ')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('** **', '')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('** **', '')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('** **', '')
        self.paragraph_text_with_artifacts = self.paragraph_text_with_artifacts.replace('** **', '')

    def __str__(self):
        return self.paragraph_text

    def str_with_out_artifacts(self):
        return self.paragraph_text


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
    if len(soup.find_all(True, recursive=False)) == 0:
        current_h1.append(Paragraph(soup))
    return current_h1


def tokenize_data(text):
    tokens = word_tokenize(text, language="russian")
    snowball = SnowballStemmer(language="russian")
    filtered_tokens = []
    for token in tokens:
        if token not in STOP_WORDS and len(token) > 2:
            filtered_tokens.append(snowball.stem(token))
    return filtered_tokens
