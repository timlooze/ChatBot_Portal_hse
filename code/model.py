import pickle
import numpy.random as rd
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from test_generator import TestGeneration

"""
Model itself that predicts the answer, based on training data
"""


class Model:

    # Initializing test data and necessary tokens for the multiple model of prediction
    def __init__(self, loaded, levels=None, levels_tokenize=None, links=None):
        if loaded:
            self.model = pickle.load(open("../tg_bot_files/model.pickle", "rb"))
            self.target_unmap = pickle.load(open("../tg_bot_files/target_unmap.pickle", "rb"))
            self.levels = pickle.load(open("../tg_bot_files/levels.pickle", "rb"))
            self.links = pickle.load(open("../tg_bot_files/links.pickle", "rb"))
            return
        self.model = Pipeline([
            ('vect', CountVectorizer()),
            ('tfid', TfidfTransformer()),
            ('clf', MLPClassifier(random_state=1, max_iter=100))])
        self.levels = levels
        self.links = links
        self.tests = TestGeneration.get_test
        pairs = []
        num = 0
        self.target_map = dict()
        self.target_unmap = dict()
        for first in range(len(levels_tokenize[4])):
            for second in range(len(levels_tokenize[4][first])):
                for third in range(len(levels_tokenize[4][first][second])):
                    for fourth in range(len(levels_tokenize[4][first][second][third])):
                        for fifth in range(len(levels_tokenize[4][first][second][third][fourth])):
                            elem = levels_tokenize[4][first][second][third][fourth][fifth]
                            if not elem:
                                continue
                            self.target_map[(first, second, third, fourth, fifth)] = num
                            self.target_unmap[num] = (first, second, third, fourth, fifth)
                            num += 1
                            for _ in range(25):
                                pairs.append((' '.join(rd.choice(elem, rd.randint(3, 10))),
                                              (first, second, third, fourth, fifth)))
        df = pd.DataFrame(pairs, columns=['data', 'target'])
        self.X = df.data
        self.y = df.target.map(self.target_map)

    # Returns data
    def getXY(self):
        return self.X, self.y

    # Fits prediction
    def fit(self, x_train, y_train):
        self.model.fit(x_train, y_train)

    # Prediction
    def predict(self, x_test):
        pred = self.target_unmap[self.model.predict([x_test])[0]]
        text = self.levels[4][pred[0]][pred[1]][pred[2]][pred[3]][pred[4]]
        link = self.links[pred[0]]
        return text, link

    # Saves model for telegram bot
    def save(self):
        pickle.dump(self.model, open("../tg_bot_files/model.pickle", "wb"))
        pickle.dump(self.target_unmap, open("../tg_bot_files/target_unmap.pickle", "wb"))
        pickle.dump(self.levels, open("../tg_bot_files/levels.pickle", "wb"))
        pickle.dump(self.links, open("../tg_bot_files/links.pickle", "wb"))
