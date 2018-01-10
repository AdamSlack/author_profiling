from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
from nltk.data import load
from functools import reduce
import string
from json import dumps
from itertools import product
from collections import defaultdict

def parse_emo_lex():
    """ parses emotive lexicon into dict of words with a dict of their emotive tags """
    emolex = defaultdict(lambda : defaultdict(int))
    with open('../data/emolex.tsv') as f:
        for line in f:
            components = line.strip().split('\t')
            try:
                emolex[components[0]][components[1]] = int(components[2])
            except:
                print(line)
                print(components)
                raise
    return emolex

def emo_lex_emotions(emo_lex = None):
    if not emo_lex:
        emo_lex = parse_emo_lex()

    return list(emo_lex[list(emo_lex.keys())[0]].keys())
    
def upenn_tags():
    tag_dict = load('help/tagsets/upenn_tagset.pickle')
    return list(tag_dict.keys())

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
    n = count_words(tokenized_review)
    total = count_word_characters(tokenized_review)
    return total/n

def process_review(review : str):
    """ derive numerical variables from a given review string """
    tokenized_review = tokenize(review)
    sent_count = count_sentences(tokenized_review)

def pos_tag_review(tokenized_review : 'list of list of str'):
    """ perform pos tagggin on each sentence in a review """
    return [pos_tag(sent) for sent in tokenized_review]

def count_unigrams(tokenized_review : 'list of list of str'):
    """ count the unigrams present in each sentence of a review"""
    tag_set = upenn_tags()
    unigram_counts = {tag: 0 for tag in tag_set}
    tagged_review = pos_tag_review(tokenized_review)
    for sent in tagged_review:
        for word in sent:
            unigram_counts[word[1]] += 1
    return unigram_counts

def count_bigrams(tokenized_review : 'list of list of str'):
    tag_set = upenn_tags()
    bigram_counts = {format_bigram_key(tag[0], tag[1]): 0 for tag in product(tag_set,repeat=2)}
    tagged_review = pos_tag_review(tokenized_review)

    for sent in tagged_review:
        for idx in range(0, len(sent)-2):
            x = sent[idx][1]
            y = sent[idx + 1][1]
            bigram_counts[format_bigram_key(x, y)] += 1

    return bigram_counts

def format_bigram_key(first : str, second : str):
    return r'{}/{}'.format(first, second)

def format_trigram_key(first : str, second : str, third : str):
    return r'{}/{}/{}'.format(first, second, third)

def count_trigrams(tokenized_review : 'list of list of str'):
    tag_set = upenn_tags()
    trigram_counts = {format_trigram_key(tag[0], tag[1], tag[2]) : 0 for tag in product(tag_set,repeat=3)}
    tagged_review = pos_tag_review(tokenized_review)

    for sent in tagged_review:
        for idx in range(0, len(sent)-3):
            x = sent[idx][1]
            y = sent[idx + 1][1]
            z = sent[idx + 2][1]
            trigram_counts[format_trigram_key(x,y,z)] += 1   
    return trigram_counts

def emotive_scores(tokenized_review : 'list of list of str', emo_lex=None):
    if not emo_lex:
        emo_lex = parse_emo_lex()

    review_emotive_counts = {emote : 0 for emote in emo_lex_emotions(emo_lex)}

    for sent in tokenized_review:
        for word in sent:
            if word.lower() in emo_lex:
                for key, val in emo_lex[word.lower()].items():
                    review_emotive_counts[key] += val

    return review_emotive_counts

def sentiment_score(tokenized_review : 'list of list of str', emo_lex=None, emotive_scores=None ):
    if not emo_lex and not emotive_scores:
        emo_lex = parse_emo_lex()

    if not emotive_scores:
        emotive_scores = emotive_scores(tokenized_review, emo_lex)

    pos = emotive_scores['positive']
    neg = emotive_scores['negative']

    return (pos - neg) / (pos + neg)

def main():
    """ main program flow. """
    review = 'The book was brilliant, i really enjoyed reading it. It was delightful to be presented with characters as developed as those in this story. The author was masterful in their ability to craft a world so full of wonders. The only critisism that i have is that it was not long enough, i am distressed to think that the story is already over.'

    # review init
    tokenized_review = tokenize(review)
    print(review)
    print('Tokens: ')
    print(tokenized_review)

    # Surface Stats
    #word_count = count_words(tokenized_review)
    #sent_count = count_sentences(tokenized_review)
    #avg_sent_len = average_sentence_length(tokenized_review)
    #char_count = count_word_characters(tokenized_review)
    #avg_word_len = average_word_length(tokenized_review)
    #print('Word Count:', str(word_count))
    #print('Sent Count:', str(sent_count))
    #print('Average Sentence Length:', str(avg_sent_len))
    #print('Character Count:', str(char_count))
    #print('Average Word Length:', str(avg_word_len))3

    # POS Tag Stats
    #unigram_counts = count_unigrams(tokenized_review)
    #bigram_counts = count_bigrams(tokenized_review)
    #trigram_counts = count_trigrams(tokenized_review)
    #print(dumps(unigram_counts,indent=2))
    #print(dumps(bigram_counts,indent=2))
    #print(dumps(trigram_counts, indent=2))

    # Emotive Stats
    emo_lex = parse_emo_lex()
    review_emotive_counts = emotive_scores(tokenized_review, emo_lex)
    review_sentiment_score = sentiment_score(tokenized_review, emotive_scores=review_emotive_counts)
    #print(emo_lex_emotions(emo_lex))
    #print(dumps(review_emotive_counts,indent=2))
    #print('Sentiment Score: ' + str(review_sentiment_score))


if __name__ == '__main__':
    main()
