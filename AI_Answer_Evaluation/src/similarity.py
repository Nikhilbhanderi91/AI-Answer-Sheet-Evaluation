from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(ans1, ans2):
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([ans1, ans2])

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    return similarity