import db as db
from nltk import word_tokenize
from collections import defaultdict
import json

GLOBAL_WORDS = defaultdict(int)

def consume_review(rev):
    """ tokenises a review and adds words to a set of words """
    tokens = word_tokenize(rev)

    for t in tokens:
        GLOBAL_WORDS[str(t).upper()] += 1


def main():
    conn = db.connect_to_db(host='localhost', dbname='tonicwater', user='postgres', password='password')

    reviews = db.select_all_reviews(conn)
    count = 0
    print('vectorising corpus word occurences')
    for rev in reviews:
        text = rev[2]
        consume_review(text)
        count += 1
        if count % 500 == 0:
            print('Words:' + str(len(GLOBAL_WORDS)) + ' Rev Count: ' + str(count))

    print(GLOBAL_WORDS)

    with open('../data/words.json', 'w') as f:
        f.write(json.dumps(GLOBAL_WORDS, sort_keys=True, indent=4))

if __name__ == '__main__':
    main()