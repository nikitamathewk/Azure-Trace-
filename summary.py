import nltk
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from scipy.sparse.linalg import svds
import networkx
nltk.download('punkt')
nltk.download('stopwords')

def create_summary(review):
    DOCUMENT = str(review)
    DOCUMENT = re.sub(r'\n|\r', ' ', DOCUMENT)
    DOCUMENT = re.sub(r' +', ' ', DOCUMENT)
    DOCUMENT = DOCUMENT.strip()
    sentences = nltk.sent_tokenize(DOCUMENT)
    stop_words = nltk.corpus.stopwords.words('english')

    def normalize_document(doc):
        doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I|re.A)
        doc = doc.lower()
        doc = doc.strip()
        tokens = nltk.word_tokenize(doc)
        filtered_tokens = [token for token in tokens if token not in stop_words]
        doc = ' '.join(filtered_tokens)
        return doc

    normalize_corpus = np.vectorize(normalize_document)
    norm_sentences = normalize_corpus(sentences)

    tv = TfidfVectorizer(min_df=0., max_df=1., use_idf=True)
    dt_matrix = tv.fit_transform(norm_sentences)
    dt_matrix = dt_matrix.toarray()
    vocab = tv.get_feature_names()
    td_matrix = dt_matrix.T
    pd.DataFrame(np.round(td_matrix, 2), index=vocab).head(10)
    
    def low_rank_svd(matrix, singular_count=2):
        u, s, vt = svds(matrix, k=singular_count)
        return u, s, vt

    num_sentences = 8
    num_topics = 3
    u, s, vt = low_rank_svd(td_matrix, singular_count=num_topics)  
    term_topic_mat, singular_values, topic_document_mat = u, s, vt

    sv_threshold = 0.5
    min_sigma_value = max(singular_values) * sv_threshold
    singular_values[singular_values < min_sigma_value] = 0

    salience_scores = np.sqrt(np.dot(np.square(singular_values), np.square(topic_document_mat)))

    top_sentence_indices = (-salience_scores).argsort()[:num_sentences]
    top_sentence_indices.sort()

    similarity_matrix = np.matmul(dt_matrix, dt_matrix.T)
    similarity_graph = networkx.from_numpy_array(similarity_matrix)
    scores = networkx.pagerank(similarity_graph)
    ranked_sentences = sorted(((score, index) for index, score in scores.items()), reverse=True)

    top_sentence_indices = [ranked_sentences[index][1] for index in range(num_sentences)]
    top_sentence_indices.sort()

    # print('\n'.join(np.array(sentences)[top_sentence_indices]))
    summ1 = np.array(sentences)[top_sentence_indices]
    summ = ""
    for i in summ1:
        summ=summ+i+" "

    return summ