import numpy as np
import pandas as pd
import torch
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
import ast
from sklearn.model_selection import train_test_split
import torch.nn as nn
import random
import torch.nn.functional as F
from torch.autograd import Variable
from torch.utils.data import DataLoader, TensorDataset
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def to_tensor(np_ms):
    return torch.tensor(np_ms, dtype=torch.float, device=DEVICE)


dictionary = []
file = pd.read_excel('../data_files/levels_tokenize_1.xlsx')
for j in file.index:
    dictionary += file.iloc[j][1:].drop_duplicates().dropna().to_list()
education_data = pd.DataFrame(np.zeros(len(dictionary)).reshape(1, -1))
education_data.columns = dictionary
test = pd.read_excel('../data_files/train_set.xlsx')
nameing_dict = {}
number = 0
for i in dictionary:
    nameing_dict[i] = number
    number += 1
matrix_data_X = np.zeros((test.shape[0], education_data.shape[1]))

for i in range(test.shape[0]):
    for j in test.loc[i, 'text'].split():
        if j in dictionary:
            matrix_data_X[i][nameing_dict[j]] += 1

print("preapring finished")
X = [i for i in matrix_data_X]
y = [(''.join([str(i) for i in ast.literal_eval(x)])) for x in test['index'].to_list()]
print("calculating neyron")
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, shuffle=True, random_state=1)
clf = MLPClassifier(random_state=1, max_iter=100).fit(X_train, y_train)
print(clf.score(X_test, y_test))
