from tokenize_data import tokenize_data
from model import Model


def main():
    new_text = 'что делать'
    new_text = ' '.join(tokenize_data(new_text))
    model = Model(True)
    print(model.predict(new_text))


main()
