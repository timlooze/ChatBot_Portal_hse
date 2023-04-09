"""
Class for finding the best answer on the question of the user
"""
import numpy as np
import pandas as pd
from tqdm import tqdm


class Finder:
    """
    Initialization of the list of texts on portal
    """

    def __init__(self):
        from linkgraph import LinkGraph
        self.sentence_embeddings = [  # pd.read_excel('../data_files/level_1.xlsx'),
            pd.read_excel('../data_files/level_2.xlsx'),
            pd.read_excel('../data_files/level_3.xlsx'),
            pd.read_excel('../data_files/level_4.xlsx'),
            pd.read_excel('../data_files/level_5.xlsx')]
        # Function from library to create SBERT word comparator
        from sentence_transformers import SentenceTransformer
        # SBERT model itself
        # List of texts on portal pages

    """
    Function to find the best answer for the question
    """

    def guess(self, question, file_num = 0):
        from sklearn.metrics.pairwise import cosine_similarity
        from sentence_transformers import SentenceTransformer
        scores = []
        # for y in range(self.sentence_embeddings[file_num].shape[0]):
        for x in tqdm(range(self.sentence_embeddings[file_num].shape[0])):
            model = SentenceTransformer('bert-base-nli-mean-tokens')
            sentences = model.encode(self.sentence_embeddings[file_num].iloc[x].tolist() + [question])
            # text_scores = np.zeros((sentences.shape[0], sentences.shape[0]))
            # for j in range(sentences.shape[0]):
            #     text_scores[j, :] = np.array(cosine_similarity([sentences[-1]], sentences))

            scores.append(cosine_similarity([sentences[-1]], sentences))
        # return self.sentence_embeddings[np.argmax(scores[:-2][-1])], np.max(scores[:-2][-1])
        return (scores)


print('finder')
