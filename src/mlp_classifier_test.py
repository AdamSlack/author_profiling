from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import normalize 
import numpy as np

from preprocess import *

def main():
    """ Main Process Flow """    
    reviews = [
        'This is a test review, it has positive information in it. The results of this should be absolutely wonderful. Only happiness, smiles and sunshine from here on out!',
        'Negative review. I hated this book. it was miserable and sad, not at all what i wanted to be reading. It is also poorly written and structured.',
        'Happy, Sad, Angry, Delighted. This book was a rollercoaster of emotions. I wanted to laught, and i wanted to cry. Stellar writing from an amazing author.',
        'What can i say? This book is just plain awful. Terrible does not quite describe the extent of how bad this book is. Do not read. It is bad.',
        'This book was okay, it is short enough that you can tolerate some of its quirks. If it was anylonger, then those same quirks would have driven me insane. Average book, Average characters, Average.',
        'What is life, this book makes you yearn for greater answers. Master piece, 10 out of 10.'
        ]

    authors = ['Adam', 'Adam', 'Adam', 'Rachael', 'Rachael', 'Rachael']
    author_ids = [0,0,0,1,1,1]
    data = np.array([d.data() for d in process_reviews(reviews)])

    print(data.shape)

    norm_data = normalize(data, 'l2')

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(norm_data, author_ids)

    test_reviews = [
        'I Hate This, The Film Is Bad, the Book Is Worse.',
        'This is a Positive Review, Full of happiness and joy. The book was great, would recommed. The most interesting characters were also the most evil.'
    ]
    test_data = np.array([d.data() for d in process_reviews(test_reviews)])
    res = clf.predict(test_data)
    print(res)


if __name__ == '__main__':
    main()
