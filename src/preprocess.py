from data_stats import *
from db import *
from json import dumps
import numpy as np

class ProcessedReview:
    
    def __init__(self, tokens, word_count, sent_count, avg_sent_len, avg_word_len, unigram_counts, bigram_counts, trigram_counts, emotive_counts, sentiment_score):
        """ Class constructor """
        self.tokens = tokens
        self.word_count = word_count
        self.sent_count = sent_count
        self.avg_sent_len = avg_sent_len
        self.avg_word_len = avg_word_len
        self.unigram_counts = unigram_counts
        self.bigram_counts = bigram_counts
        self.trigram_counts = trigram_counts
        self.emotive_counts = emotive_counts
        self.sentiment_score = sentiment_score
    
    def __str__(self):
        return 'Tokens: ' + dumps(self.tokens) + '\n' + \
               'Word Count: ' + str(self.word_count) + '\n' + \
               'Average Word Length: ' + str(self.avg_word_len) + '\n' + \
               'Sentence Count: ' + str(self.sent_count) + '\n' \
               'Average Sentence Length: ' + str(self.avg_sent_len) + '\n' + \
               'Emotive Counts:\n' + dumps(self.emotive_counts, indent=2) + '\n' + \
               'Sentiment Score: ' + str(self.sentiment_score) + '\n'

    def db_tuple(self, id, author_name):
        return (
            id,
            author_name,
            dumps(self.tokens),
            self.word_count,
            self.sent_count,
            self.avg_sent_len,
            self.avg_word_len,
            dumps(self.unigram_counts),
            dumps(self.bigram_counts),
            dumps(self.trigram_counts),
            dumps(self.emotive_counts),
            self.sentiment_score
        )

    def data_columns(self):
        cols = [
            'word_count' ,
            'sent_count',
            'avg_sent_len',
            'avg_word_len',
            'sentiment_score'
        ]
        uni = list(self.unigram_counts.keys())
        bi = list(self.bigram_counts.keys())
        emo = list(self.emotive_counts.keys())

        return cols + uni + bi + emo

    def data(self):
        data = [
            self.word_count,
                self.sent_count,
                self.avg_sent_len,
                self.avg_word_len,
                self.sentiment_score
        ]

        uni = list(self.unigram_counts.values())
        bi  = list(self.bigram_counts.values())
        tri = list(self.trigram_counts.values())
        emo = list(self.emotive_counts.values())
    
        return data + uni + bi + emo

    def dict_components(self, review_dict):
        labels = list(review_dict.keys())
        values = [review_dict[key] for key in labels]

        return labels, values

    def label_array_tsv_string(self, arr):
        s = arr[0]
        for v in range (1, len(arr)-1):
            s += '\t' + arr[v]

        return s
    
    def value_array_tsv_string(self, arr):
        s = str(arr[0])
        for v in range (1, len(arr)-1):
            s += '\t' + str(arr[v])
        return s

    def to_tsv(self, id, author_name):
        unigram_labels, unigram_values = self.dict_components(self.unigram_counts)
        bigram_labels, bigram_values = self.dict_components(self.bigram_counts)
        trigram_labels, trigram_values = self.dict_components(self.trigram_counts)
        emotive_labels, emotive_values = self.dict_components(self.emotive_counts)

        labels = 'id\tname\tword._count\tsent_count\tavg_sent_len\tavg_word_len\t'
        labels += self.label_array_tsv_string(unigram_labels) + '\t'
        labels += self.label_array_tsv_string(bigram_labels) + '\t'
        labels += self.label_array_tsv_string(trigram_labels) + '\t'
        labels += self.label_array_tsv_string(emotive_labels) + '\t'

        labels += 'sentiment_score'

        values = str(id) + '\t' + str(author_name) + '\t' + str(self.word_count) + '\t' + str(self.sent_count) + '\t' + str(self.avg_sent_len)  + '\t' + str(self.avg_word_len) + '\t'

        values += self.value_array_tsv_string(unigram_values) + '\t'
        values += self.value_array_tsv_string(bigram_values) + '\t'
        values += self.value_array_tsv_string(trigram_values) + '\t'
        values += self.value_array_tsv_string(emotive_values) + '\t'       
        return labels, values        

    def value_array(self):
        unigram_labels, unigram_values = self.dict_components(self.unigram_counts)
        bigram_labels, bigram_values = self.dict_components(self.bigram_counts)
        trigram_labels, trigram_values = self.dict_components(self.trigram_counts)
        emotive_labels, emotive_valuesdata_stats = self.dict_components(self.emotive_counts)
    


def process_review(review_string):
    """ process a review, deriving numerical variables from the string. """
    tokenized_review = tokenize(review_string)
    
    word_count = count_words(tokenized_review)
    sent_count = count_sentences(tokenized_review)
    avg_sent_len = average_sentence_length(tokenized_review)
    char_count = count_word_characters(tokenized_review)
    avg_word_len = average_word_length(tokenized_review)

    unigram_counts = count_unigrams(tokenized_review)
    bigram_counts = count_bigrams(tokenized_review)
    trigram_counts = count_trigrams(tokenized_review)

    emo_lex = parse_emo_lex()
    review_emotive_counts = emotive_scores(tokenized_review, emo_lex)
    review_sentiment_score = sentiment_score(tokenized_review, emotive_scores=review_emotive_counts)

    return ProcessedReview(tokenized_review, word_count, sent_count, avg_sent_len, avg_word_len, unigram_counts, bigram_counts, trigram_counts, review_emotive_counts, review_sentiment_score)

def process_reviews(reviews):
    """ given an array of reviews, return array of derived data """
    return [process_review(review) for review in reviews]

def main():
    """ Main Program Execution. """
    test_reviews = [
        'This is a test review, it has positive information in it. The results of this should be absolutely wonderful. Only happiness, smiles and sunshine from here on out!',
        'Negative review. I hated this book. it was miserable and sad, not at all what i wanted to be reading. It is also poorly written and structured.',
        'Happy, Sad, Angry, Delighted. This book was a rollercoaster of emotions. I wanted to laught, and i wanted to cry. Stellar writing from an amazing author.',
        'What can i say? This book is just plain awful. Terrible does not quite describe the extent of how bad this book is. Do not read. It is bad.',
        'This book was okay, it is short enough that you can tolerate some of its quirks. If it was anylonger, then those same quirks would have driven me insane. Average book, Average characters, Average.'
        ]

    #db = connect_to_db(host='localhost',dbname='tonicwater',user='postgres',password='password')

    # print('Inserting Review')
    # for idx, rev in enumerate(test_reviews):
    #    if not insert_review(db=db, author_name=str(idx), review=rev, rating=idx):
    #        print('Failed to insert review.')
    #        break

    
    proc = process_review(test_reviews[0])
    print(proc.data_columns())

    # values = []
    # labels = ''
    # print('Processing Reviews')
    # for review in select_all_reviews(db):
    #     review_id = review[0]
    #     author_name = review[1]
    #     review_string = review[2]
    #     processed_review = process_review(review_string)
    #     insert_processed_review(db, processed_review.db_tuple(review_id, author_name))
    #     l,v = processed_review.to_tsv(review_id, author_name)
    #     labels = l
    #     values.append(v)

    # with open('foo.tsv', 'w') as f:
    #     f.write(labels + '\n')
    #     for line in values:
    #         f.write(line + '\n')
if __name__ == '__main__':
    main()
