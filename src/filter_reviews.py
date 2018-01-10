import db as db
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
from collections import defaultdict

STOP_WORDS = defaultdict(set)

def init_stopwords():
    """ initialises global STOP_WORDS variable"""
    for lang in stopwords.fileids() :
        STOP_WORDS[lang] = set(stopwords.words(lang)[0:50])

def valid_rating(rating):
    return (rating > -1 and rating < 11)

# Adapted from http://blog.alejandronolla.com/2013/05/15/detecting-text-language-with-python-and-nltk/
def is_english(review):
    """ Checks if a review is written in english or not."""
    review_tokens = set(wordpunct_tokenize(review))
    lang_occur = defaultdict(int)
    for key in STOP_WORDS.keys():
        intersect = review_tokens.intersection(STOP_WORDS[key])
        lang_occur[key] = len(intersect)
    
    max_lang = max(lang_occur, key=lang_occur.get)
    return (max_lang == 'english' and lang_occur['english'] > 0)

def main():
    """ Main Function """
    init_stopwords()

    conn = db.connect_to_db(host='localhost', dbname='tonicwater', user='postgres', password='password')

    all_reviews = db.select_all_reviews(conn)

    print('Checking Reviews Now...')
    for rev in all_reviews:
        author = rev[5]
        review = rev[9]
        rating = rev[10]

        if valid_rating(rating) and is_english(review):
            res = db.insert_review(conn, author, review, rating)
            if not res:
                print('Record not inserted.')

    #if res:
    #    print('WIN!')
    #else:
    #    print('FAIL')
    #print(one[5] + '\n\n' + one[9] + '\n\n' + str(one[10]))

def alt_main():
    is_english('This is an English text. It\'s made up of English words.')

if __name__ == "__main__":
    alt_main()
