import numpy as np
import openpyxl
import pandas as pd

from finder import Finder


# from textparser import Paragraph

def main():
    game = Finder()
    a = input()
    # a = pd.read_excel('../data_files/level_1.xlsx').reset_index(drop = True)
    # a.columns = [['ind', 'text']]
    b = np.array(game.guess(a))
    b.reshape(37, -1)
    pd.DataFrame(b).to_excel('../data_files/scores.xlsx')
    print(b)

main()
# print(pd.read_excel('../data_files/level_2.xlsx').iloc[np.argmax(pd.read_excel('../data_files/scores.xlsx')[0])])
# print(pd.read_excel('../data_files/scores.xlsx')[0].max())
# print(np.zeros(pd.read_excel(f'../data_files/level_2.xlsx').shape))
# from linkgraph import LinkGraph
# sentence_embeddings = LinkGraph()
# question = ''
#
# while question != 0:
#     question = input()
#
#     sentence_embeddings_list = ['fuck you', 'suck dick', 'little pussy']
#     sentence_embeddings_list.append(question)
#     print(sentence_embeddings_list)
#     from sentence_transformers import SentenceTransformer
#
#     model = SentenceTransformer('bert-base-nli-mean-tokens')
#     sentence_embeddings = model.encode(sentence_embeddings_list)
#     from sklearn.metrics.pairwise import cosine_similarity
#
#     scores = cosine_similarity([sentence_embeddings[-1]], sentence_embeddings)[0]
#
#     print(sentence_embeddings_list[np.argmax(scores[:-1])], np.max(scores[:-1]))
