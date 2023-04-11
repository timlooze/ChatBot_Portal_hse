import numpy.random as rd
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


class Model:
    def __init__(self, levels, levels_tokenize, links):
        self.model = Pipeline([
            ('vect', CountVectorizer()),
            ('tfid', TfidfTransformer()),
            ('clf', MLPClassifier(random_state=1, max_iter=100))])
        self.levels = levels
        self.links = links
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

    def getXy(self):
        return self.X, self.y

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        pred = self.target_unmap[self.model.predict([X_test])[0]]
        text = self.levels[4][pred[0]][pred[1]][pred[2]][pred[3]][pred[4]]
        link = self.links[pred[0]]
        return text, link

    def save(self):
        filename = "model.joblib"
        joblib.dump(self.model, filename)
