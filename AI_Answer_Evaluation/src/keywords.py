from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def extract_keywords(text):
    words = text.lower().split()

    # Remove stopwords
    keywords = [word for word in words if word not in ENGLISH_STOP_WORDS]

    return list(set(keywords))


def keyword_score(student_ans, keywords):
    student_words = student_ans.lower().split()

    match_count = 0

    for word in keywords:
        if word in student_words:
            match_count += 1

    if len(keywords) == 0:
        return 0

    return match_count / len(keywords)