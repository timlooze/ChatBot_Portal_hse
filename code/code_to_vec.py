"""
Class for finding the best answer on the question of the user
"""


class Finder:
    """
    Initialization of the list of texts on portal
    """
    def __init__(self, sentence_embeddings):
        # Function from library to create SBERT word comparator
        from sentence_transformers import SentenceTransformer
        # SBERT model itself
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        # List of texts on portal pages
        self.sentence_embeddings = model.encode(sentence_embeddings)
    """
    Function to find the best answer for the question
    """
    def guess(self, question):
        # Comparing function from the sklearn
        from sklearn.metrics.pairwise import cosine_similarity
        # Scores of equality of the questions
        scores = cosine_similarity([question], self.sentence_embeddings)[0]
        return scores
