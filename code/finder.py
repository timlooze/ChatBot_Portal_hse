"""
Class for finding the best answer on the question of the user
"""
import numpy as np


class Finder:
    """
    Initialization of the list of texts on portal
    """

    def __init__(self):
        from linkgraph import LinkGraph
        sentence_embeddings = LinkGraph().get_link_text()
        # Function from library to create SBERT word comparator
        from sentence_transformers import SentenceTransformer
        # SBERT model itself
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')
        # List of texts on portal pages
        self.sentence_embeddings = sentence_embeddings

    """
    Function to find the best answer for the question
    """

    def guess(self, question):
        # Comparing function from the sklearn
        from sklearn.metrics.pairwise import cosine_similarity
        from sentence_transformers import SentenceTransformer
        # Scores of equality of the questions
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')
        sentences = self.model.encode(self.sentence_embeddings + [question])
        scores = np.zeros((sentences.shape[0], sentences.shape[0]))
        for i in range(sentences.shape[0]):
            scores[i, :] = cosine_similarity([sentences[i]], sentences)[0]
        # scores = cosine_similarity([sentences[-1]], sentences)[0]

        # return self.sentence_embeddings[np.argmax(scores[:-2][-1])], np.max(scores[:-2][-1])

        return scores


print('finder')
