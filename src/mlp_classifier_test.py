from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import normalize 

import numpy as np
from copy import deepcopy

from preprocess import *
from db import *

def enumerate_review_authors(processed_reviews):
    """ Given an array of ProcessedReview objects, create an dict of the author names and idx """

    return {auth: idx for idx, auth in enumerate(list(set([rev.author for rev in processed_reviews])))}

def enumerate_class_options(classifications):
    """ given an array of possible classifications, return an enum for each possivle class """
    return {c: idx for idx, c in enumerate(list(set([c for c in classifications])))}

def retrieve_review_data(batch_size, offset):
    """ fetch reviews from database and create array of authors and array of reviews. """
    conn = connect_to_db('localhost', 'tonicwater', 'postgres', 'password')
    revs = select_filtered_reviews(conn, batch_size, offset)

    reviews = []
    authors = []
    
    for rev in revs:
        authors.append(rev[1])
        reviews.append(process_review(rev[2]).data())    

    return authors, reviews

def map_author_index(authors, author_enum):
    """ given an array of author strings, find the enum value for it """

    return [author_enum[auth] for auth in authors]

def main():
    """ Main Process Flow """    

    authors, reviews = retrieve_review_data(100, 0)
        
    norm_reviews = normalize(reviews, 'l2')

    print(len(authors), len(reviews))

    reviews_c = deepcopy(norm_reviews.tolist())
    del reviews_c[10]
    del reviews_c[15]

    training_reviews = np.array(reviews_c)

    auth_c = deepcopy(authors)
    del auth_c[10]
    del auth_c[15]

    auth_enum = enumerate_class_options(authors)
    training_auth = map_author_index(auth_c, auth_enum)

    print(training_auth)
    print(training_reviews.shape)


    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(training_reviews, training_auth)

    print('Actual:', map_author_index([authors[10],authors[15]], auth_enum))

    test_data = np.array([norm_reviews[10], norm_reviews[15]])
    res = clf.predict(test_data)
    print('Predicted:', res)


if __name__ == '__main__':
    main()
