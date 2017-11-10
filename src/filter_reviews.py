import db as db

def main():
    """ Main Function """
    conn = db.connect_to_db(host='localhost', dbname='tonicwater', user='postgres', password='password')

    all_reviews = db.select_all_reviews(conn)

    one = all_reviews.fetchone()
    res = db.insert_review(conn, one[5], one[9], one[10])
    if res:
        print('WIN!')
    else:
        print('FAIL')
    print(one[5] + '\n\n' + one[9] + '\n\n' + str(one[10]))


if __name__ == "__main__":
    main()
