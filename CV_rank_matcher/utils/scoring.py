from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(text1, text2):
    """
    Compute cosine similarity between two texts
    """
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(vectors)[0,1]

def skill_score(text, keywords):
    """
    Count keyword matches in text for a simple skill score
    """
    score = 0
    text_lower = text.lower()
    for word in keywords:
        if word.lower() in text_lower:
            score += 1
    return score
