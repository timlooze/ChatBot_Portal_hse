from nltk.tokenize import word_tokenize
import nltk
from nltk.stem import SnowballStemmer

nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords

STOP_WORDS = stopwords.words("russian")


def tokenize_data(text):
    tokens = word_tokenize(text, language="russian")
    snowball = SnowballStemmer(language="russian")
    filtered_tokens = []
    for token in tokens:
        if token not in STOP_WORDS and len(token) > 2:
            filtered_tokens.append(snowball.stem(token))
    return filtered_tokens
