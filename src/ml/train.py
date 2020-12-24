from typing import List, AnyStr

from . import data

def calculate_lsa(corpus: List[AnyStr]):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    from sklearn.decomposition import TruncatedSVD
    
    # TODO: Scale this later, it performs everything in memory currently

    # Calculate TfIdf
    vectorizer = TfidfVectorizer(stop_words=ENGLISH_STOP_WORDS)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Calculate SVD
    k = 100 # Dimension being reduced to
    # TODO: Check against different values of k to evaluate 
    svd = TruncatedSVD(n_components=k)
    X_k = svd.fit_transform(tfidf_matrix)

    # Get topics out of matrices
    terms = vectorizer.get_feature_names()
    term_matrix = svd.components_ # shape (n_components, n_features)
    for i, c in enumerate(term_matrix):
        tc = zip(term_matrix, c)
        for t in tc:
            print(t)
    
    data.save_document_topics()