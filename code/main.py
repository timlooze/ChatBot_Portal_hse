import numpy as np
import pandas as pd

# from finder import Finder

import openpyxl

from textparser import Paragraph


def get_on_depth(header, n):
    if n == 1 or type(header) == Paragraph or len(header.objects) == 0:
        res = header.__str__()
        for i in range(n - 1):
            res = [res]
        return res
    else:
        objects = []
        for o in header.objects:
            objects.append(get_on_depth(o, n - 1))
        return objects


def main():
    # game = Finder()
    # a = input()
    from linkgraph import LinkGraph
    sentence_embeddings = LinkGraph().get_link_text()
    level_1 = []
    level_2 = []
    level_3 = []
    level_4 = []
    level_5 = []
    for i in sentence_embeddings:
        level_1.append(get_on_depth(i, 1))
        level_2.append(get_on_depth(i, 2))
        level_3.append(get_on_depth(i, 3))
        level_4.append(get_on_depth(i, 4))
        level_5.append(get_on_depth(i, 5))
    t = 0
    for i in level_2:
        for j in i:
            t += 1
    print(t)
    t = 0
    for i in level_5:
        for j in i:
            for k in j:
                for p in k:
                    for m in p:
                        t += 1
    print(t)
    levels = [level_1, level_2, level_3, level_4, level_5]
    for i, level in enumerate(levels):
        pd.DataFrame(level).to_excel(f'level_{i+1}.xlsx')


main()

from linkgraph import LinkGraph
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
