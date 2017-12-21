from nltk.tokenize import sent_tokenize, word_tokenize
from functools import reduce
import string

def tokenize(review : str):
    """ tokenizes a review string into sents and words """
    sents = sent_tokenize(review)
    return [word_tokenize(sent) for sent in sents ]

def count_sentences(tokenized_review : 'list of list of str'):
    """ counts the number of sentences in a tokenized review"""
    return len(tokenized_review)

def filter_puct_tokens(tokenized_review : 'list of list of str'):
    """ filters tokens that are purely punctuation. """
    return [list(filter((lambda a: a not in string.punctuation),sent)) for sent in tokenized_review]

def count_words(tokenized_review : 'list of list of str'):
    """ counts the number of words in a tokenized review (filters punctuation tokens)"""
    review_words = filter_puct_tokens(tokenized_review) 
    return reduce( (lambda a, b: a + len(b)), review_words, 0 )

def count_word_characters(tokenized_review : 'list of list of str'):
    """ counts the total number of characters used in the words of a review. """
    review_words = filter_puct_tokens(tokenized_review)
    return reduce((lambda a, b: a + b), [reduce((lambda a, b: a + len(b)), sent, 0) for sent in review_words ],0)

def average_sentence_length(tokenized_review : 'list of list of str'):
    """ calculates the average length of sentences in a tokenized review"""
    n = len(tokenized_review)
    total = count_words(tokenized_review)
    return total/n

def average_word_length(tokenized_review : 'list of list of str'):
    """ counts the average length of words in a tokenized review"""

def process_review(review : str):
    """ derive numerical variables from a given review string """
    tokenized_review = tokenize(review)
    sent_count = count_sentences(tokenized_review)

def main():
    """ main program flow. """
    review = 'This is a sentence in a review. This is another sentence in the same review.'

    tokenized_review = tokenize(review)
    word_count = count_words(tokenized_review)
    sent_count = count_sentences(tokenized_review)
    avg_sent_len = average_sentence_length(tokenized_review)
    char_count = count_word_characters(tokenized_review)
    avg_word_len = average_word_length(tokenized_review)

    print(review)
    print('Tokens: ')
    print(tokenized_review)
    print('Word Count:', str(word_count))
    print('Sent Count:', str(sent_count))
    print('Average Sentence Length:', str(avg_sent_len))
    print('Character Count:', str(char_count))

if __name__ == '__main__':
    main()