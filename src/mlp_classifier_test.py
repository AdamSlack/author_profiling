from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import normalize 
from sklearn.utils import shuffle
import numpy as np
from copy import deepcopy

from preprocess import *
from db import *

def enumerate_review_authors(processed_reviews):
    """ Given an array of ProcessedReview objects, create an dict of the author names and idx """

    return {auth: idx for idx, auth in enumerate(list(set([rev.author for rev in processed_reviews])))}

def enumerate_class_options(classifications):
    """ given an array of pfrom sklearn.utils import shuffle
ossible classifications, return an enum for each possivle class """
    return {c: idx for idx, c in enumerate(list(set([c for c in classifications])))}

def retrieve_review_data(batch_size, offset):
    """ fetch reviews from database and create array of authors and array of reviews. """
    conn = connect_to_db('localhost', 'tonicwater', 'postgres', 'password')
    revs = select_filtered_reviews(conn, batch_size, offset)

    reviews = []
    authors = []
    
    for rev in revs:
        authors.append(rev[0])
        reviews.append(process_review(rev[1]).data())    

    return authors, reviews

def map_author_index(authors, author_enum):
    """ given an array of author strings, find the enum value for it """

    return [author_enum[auth] for auth in authors]



def calc_min_max():
    total = 430246
    steps = int(430246/500)
    authors, reviews = retrieve_review_data(1, 0)

    max_vals = reviews[0]
    min_vals = reviews[0]


    for i in range (0, steps):
        authors, reviews = retrieve_review_data(500, 1 + (i*500))
        for rev in reviews:
            max_vals = [max(max_vals[idx], var) for idx, var in enumerate(rev)]
            min_vals = [min(min_vals[idx], var) for idx, var in enumerate(rev)]

    with open('max_vals.csv') as f:
        f.writeline([str(v) + ', ' for v in max_vals])

    with open('min_vals.csv') as f:
        f.writeline([str(v) + ', ' for v in min_vals])
    

    return max_vals, min_vals    

def train_mlp(test_set_pct = 10):
    """ Train a MLP, using defined batch size and test set percentage size. """
    conn = connect_to_db('localhost', 'tonicwater', 'postgres', 'password')

    authors = select_capped_authors(conn)
    
    for author in authors:
        print('Creating Sample for:', author)

        author_reviews = [process_review(res[1]).data() for res in select_capped_author(conn, author)]
        author_review_count = len(author_reviews)
        
        other_reviews = [process_review(res[1]).data() for res in select_random_capped_reviews(conn, author_review_count, exclude=author)]
        
        print('Reviews selected for:', author, '. Author Count:', author_review_count, ' Other Count:', len(other_reviews))

        reviews = author_reviews + other_reviews
        review_classes = ([1]*author_review_count) + ([0]*author_review_count)

        print('Normalising Reviews for:', author)
        norm_reviews = normalize(reviews,'l2')

        shuffled_reviews, shuffled_classes = shuffle(norm_reviews, review_classes)

        test_set_size = int(author_review_count * (test_set_pct/50)) # div 50 as author rev count is half of total

        training_reviews = shuffled_reviews[0 : len(shuffled_reviews) - test_set_size]
        training_classes = shuffled_classes[0 : len(shuffled_classes) - test_set_size]

        test_reviews = shuffled_reviews[len(shuffled_reviews) - test_set_size : ]
        test_classes = shuffled_classes[len(shuffled_classes) - test_set_size : ]

        clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        clf.fit(training_reviews, training_classes)

        test_results = clf.predict(test_reviews)

        with open('results.txt', 'a') as f:
            f.write('Results for: ' + author + '\n\n')
            f.write('Actual: ')
            f.write(test_classes)
            f.write('\n')
            f.write('Predicted: ')
            f.write(test_results)
            f.write('\n\n\n')


def main():
    """ Main Process Flow """    


    train_mlp()
    # print(calc_min_max())
    # authors, reviews = retrieve_review_data(100, 0)
        
    # norm_reviews = normalize(reviews, 'l2')

    # print(len(authors), len(reviews))

    # reviews_c = deepcopy(norm_reviews.tolist())
    # del reviews_c[10]
    # del reviews_c[15]

    # training_reviews = np.array(reviews_c)

    # auth_c = deepcopy(authors)
    # del auth_c[10]
    # del auth_c[15]

    # auth_enum = enumerate_class_options(authors)
    # training_auth = map_author_index(auth_c, auth_enum)

    # print(training_auth)
    # print(training_reviews.shape)


    # clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    # clf.fit(training_reviews, training_auth)

    # print('Actual:', map_author_index([authors[10],authors[15]], auth_enum))

    # test_data = np.array([norm_reviews[10], norm_reviews[15]])
    # res = clf.predict(test_data)
    # print('Predicted:', res)


if __name__ == '__main__':
    main()
