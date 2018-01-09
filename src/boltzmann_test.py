from sklearn.neural_network import MLPClassifier
import numpy as np

from preprocess import *

def main():
    """ Main Process Flow """    
    test_reviews = [
        'This is a test review, it has positive information in it. The results of this should be absolutely wonderful. Only happiness, smiles and sunshine from here on out!',
        'Negative review. I hated this book. it was miserable and sad, not at all what i wanted to be reading. It is also poorly written and structured.',
        'Happy, Sad, Angry, Delighted. This book was a rollercoaster of emotions. I wanted to laught, and i wanted to cry. Stellar writing from an amazing author.',
        'What can i say? This book is just plain awful. Terrible does not quite describe the extent of how bad this book is. Do not read. It is bad.',
        'This book was okay, it is short enough that you can tolerate some of its quirks. If it was anylonger, then those same quirks would have driven me insane. Average book, Average characters, Average.'
        'What is life, this book makes you yearn for greater answers. Master piece, 10 out of 10.',
        ]

    authors = ['Adam', 'Adam', 'Adam', 'Rachael', 'Rachael', 'Rachael']
    author_ids = [0,0,0,1,1,1]
    p_revs = process_reviews(test_reviews)
    data = np.array([d.data() for d in process_reviews(test_reviews)])

    print(data.shape)


if __name__ == '__main__':
    main()
