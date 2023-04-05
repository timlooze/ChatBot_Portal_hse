import numpy as np
import pandas as pd

from finder import Finder

import openpyxl


def main():
    game = Finder()
    a = input()
    from linkgraph import LinkGraph
    sentence_embeddings = LinkGraph().get_link_text()
    pd.DataFrame(sentence_embeddings).to_excel('texts.xlsx')


# main()

from linkgraph import LinkGraph
sentence_embeddings = LinkGraph()
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
