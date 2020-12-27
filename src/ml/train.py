from typing import List, AnyStr

import numpy as np

from . import data
from .dto import ArticleDTO, TopicDTO

def calculate_lsa(corpus: List[ArticleDTO]):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    from sklearn.decomposition import TruncatedSVD
    
    # TODO: Scale this later, it performs everything in memory currently

    # Calculate TfIdf
    vectorizer = TfidfVectorizer(stop_words=ENGLISH_STOP_WORDS)
    article_content_list = [corpus[i].content for i in range(len(corpus))]
    tfidf_matrix = vectorizer.fit_transform(article_content_list)

    # Calculate SVD
    k = 100 # Dimension being reduced to
    # TODO: Check against different values of k to evaluate 
    svd = TruncatedSVD(n_components=k)
    D = svd.fit_transform(tfidf_matrix)

    # Get topics out of matrices

    articleid_topics_map = {}
    terms = vectorizer.get_feature_names()
    T = svd.components_ # shape (n_components, n_features)
    #S = svd.singular_values_

    num_topics = 5

    for i, d in enumerate(D):
        article = corpus[i]
        key = article.id

        articleid_topics_map[key] = []
        k_indexes = np.argsort(d)[:num_topics]
        components = T[k_indexes, :]

        for j, c in enumerate(components):
            term_comp = zip(terms, c)
            sorted_terms = sorted(term_comp, key=lambda x:x[1], reverse=True)[:num_topics]
            topic = TopicDTO(id=None, article_id=article.id, topic=sorted_terms[0][0])
            articleid_topics_map[key].append(topic)
    
    return articleid_topics_map