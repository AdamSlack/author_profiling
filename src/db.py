import psycopg2 as pg

def insert_review(db, author_name, review, rating):
    """ Insert an author review and rating into the DB. """
    cursor = db.cursor()
    try:
        cursor.execute("""
            insert into author_review (review_author, review, rating)
            values (%s, %s, %s)
        """, (author_name, review, rating))
    except:
        db.rollback() 
        return False

    cursor.close()
    db.commit()
    return True

def select_all_reviews(db):
    """ create a cursor for all reviews in the DB """
    cursor = db.cursor()

    cursor.execute('select * from reviews')
    return cursor

def select_reviewer_reviews(db, reviewer_name):
    """ select all reviews by a single reviewer by name."""
    cursor = db.cursor()

    cursor.execute(""" 
        select * from author_review where review_author = %s
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
