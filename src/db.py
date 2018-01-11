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

def select_all_authors(db):
    """ create a cursor for all author names in the DB """
    cursor = db.cursor()

    cursor.execute('select review_author from author_review')
    return cursor

def insert_word(db, word):
    """ Insert an word into the DB. """
    cursor = db.cursor()
    try:
        cursor.execute("""
            select count(*) from words where word = %s
        """, (word))

        res = cursor.fetchone()
        print(res)

        cursor.execute("""
            insert into words (word)
            values (%s)
        """, (word))
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

def select_filtered_reviews(db, batch_size, offset):
    """ select filtered reviews, limiting amount and offsetting """#
    print('Selecting Filtered Reviews. Batch:', batch_size, 'Offset:', offset)
    cursor = db.cursor()

    cursor.execute('select * from author_review limit %s offset %s', (batch_size, offset))
    return cursor

def select_all_filtered_reviews(db):
    """ create a cursor for all filtered reviews in the DB """

    cursor = db.cursor()

    cursor.execute('select * from author_review')
    return cursor

def select_reviewer_reviews(db, reviewer_name):
    """ select all reviews by a single reviewer by name."""
    cursor = db.cursor()

    cursor.execute(""" 
        select * from author_review where review_author = %s
    """, [reviewer_name])

    return 

def insert_processed_review(db, review_tuple):
    """ Insert the derived numerical variables of a review."""
    cursor = db.cursor()
    #try:
    cursor.execute("""
        insert into processed_reviews (
            id, 
            review_author,
            tokens, 
            word_count, 
            avg_word_length, 
            sent_count, 
            avg_sent_length, 
            unigram_counts, 
            bigram_counts, 
            trigram_counts, 
            emotive_counts, 
            sentiment_score
        ) values (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )    
    """, review_tuple)
    #except:
    #    db.rollback() 
    #    return False

    cursor.close()
    db.commit()
    return True        

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


