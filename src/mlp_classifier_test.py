from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import normalize 
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier


import time

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
    already_done = []#['jen.e.moore','JennyArch','jamespurcell','LynnB','cameling','PopcornReads','MHanover10','DLMorrese','tjsjohanna','mahallett','moonshineandrosefire','Heather19','TequilaReader']
    authors = [author for author in authors if author not in already_done]
    
    # Test author
    authors = authors[0:2]
    trained_models = []
    author_samples = []
    author_classes = []

    author_count = len(authors)
    print('Total Authors:', author_count)
    current_author_num = 0
    
    for idx, author in enumerate(authors):
        current_author_num += 1
        print('Author number: ', current_author_num, ' / ', author_count)
        print('Creating Sample for:', author)

        start_time = time.clock()
        author_reviews = [process_review(res[1]).data() for res in select_capped_author(conn, author)]
        author_samples += author_reviews
        author_classes += ([idx] * len(author_reviews))

        now_time = time.clock()
        print('Author Sample created in:', now_time - start_time)
        
        author_review_count = len(author_reviews)
        
        print('Selecting random other reviews to sample with.')
        before_time = time.clock()
        other_reviews = [process_review(res[1]).data() for res in select_random_capped_reviews(conn, author_review_count, exclude=author)]
        now_time = time.clock()
        print('Other Sample created in: ', now_time - before_time)
        print('Total Time Taken: ', now_time - start_time)
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


        # TEST CLASSIFIER
        clfs = [
            MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1, activation='relu')
        ]

        for clf in clfs:
            before_time = time.clock()
            clf.fit(training_reviews, training_classes)
            now_time = time.clock()
            print('Model Training Completed in: ',  now_time - before_time)
            print('Total Time Taken:: ', now_time - start_time)

            test_results = clf.predict(test_reviews)

            with open('compare_results.txt', 'a') as f:
                f.write('Results for: ' + author + '\n\n')
                f.write('Actual: ')
                for s in test_classes:
                    f.write('%s, ' % s)
                f.write('\n')
                f.write('Predicted: ')
                for s in test_results:
                    f.write('%s, ' % s)
                f.write('\n\n\n')

            tp = 0
            fp = 0
            tn = 0
            fn = 0

            for i in range(0, len(test_results)):
                pre = test_results[i]
                act = test_classes[i]

                if act == 1:
                    # Positive
                    if act == pre:
                        # True Positive, correct prediction
                        tp += 1
                    else:
                        # False Negative, incorrect prediction
                        fn += 1
                else:
                    # negative
                    if act == pre:
                        # True Negative, correct prediction
                        tn += 1
                    else:
                        # False Positive, incorrect prediction
                        fp += 1

            if tp == 0:
                precision = 0
                recall = 0
            else:   
                precision = tp / (tp + fp)
                recall = tp / (tp + fn)

            with open('bagging_results.csv', 'a') as f:
                f.write('%s, %s, %s, %s, %s, %s, %s\n' % (author_review_count*2, tp, fp, tn, fn, precision, recall))

            now_time = time.clock()
            print('Training Complete for: ', author)
            print('Total Time Taken for', author, ': ', now_time - start_time)

            trained_models.append(clf)

        with open('bagging_results.csv', 'a') as f:
            f.write('\n\n\n')

    eval_ensemble(trained_models, author_samples, author_classes)

def eval_ensemble(models, sample, classifications):

    shuff_sample, shuff_classes = shuffle(sample, classifications)
    
    print('Evaluating Ensemble')
    model_scores = [0] * 5

    for c, s in enumerate(shuff_sample):
        trues = 0
        falses = 0
        correct = 0
        for idx, m in enumerate(models):
            res = m.predict([s])
            if res == 0:
                falses +=1
            else:
                trues +=1 
                model_scores[idx] += 1
                if idx == shuff_classes[c]:
                    correct = 1

        with open('ensemble_results' + str(len(models)) + '.csv', 'a') as f:
            f.write('%s, %s, %s\n' % (trues, falses, correct))
    
    with open('inter_agreement' + str(len(models)) + '.csv', 'a') as f:
        f.write('%s' % len(classifications))
        for x in model_scores:
            f.write(', %s' % x)
        f.write('\n')

def main():
    """ Main Process Flow """    


    for i in range(0,100):
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
