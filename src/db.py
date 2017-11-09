import psycopg2 as pg

def main():
    """ """
    db = connect_to_db(host='localhost', dbname='tonicwater', user='postgres', password='password')

    all_reviews = select_all_reviews(db)
    print(all_reviews.fetchone())

def select_all_reviews(db):
    """ create a cursor for all reviews in the DB """
    cursor = db.cursor()

    cursor.execute('select * from reviews')
    return cursor

def select_reviewer_reviews(db, reviewer_name):
    """ select all reviews by a single reviewer by name."""
    cursor = db.cursor()

    cursor.execute(""" 
        select * from reviews where review_auther = %s
    """, [reviewer_name])

    return cursor


def connect_to_db(host, dbname, user, password):
    """ Connect to Database returning pyscopg2 cursor object """
    try:
        conn_string = "host='" + host + "' dbname='" + dbname + "' user='" + user + "' password='" + password +"'"
        
        print('Connecting to DB: ' + conn_string)
        db = pg.connect(conn_string)

        print('Connected to DB.')
        return db
    except:
        print('Unable to connect to DB')

if __name__ == "__main__":
    main()