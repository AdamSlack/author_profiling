begin;

---------------------------------------------------------------------------
-- details of each reviewer
---------------------------------------------------------------------------
create table reviewers(
    id           serial not null,
    reviewer     text   not null primary key,
    review_count int    not null
);

---------------------------------------------------------------------------
-- details of each review made by a reviewer
---------------------------------------------------------------------------
create table reviews(
    id              serial not null,
    book_title      text   not null,
    book_url        text   not null,
    book_author     text   not null,
    book_author_url text   not null,
    review_author   text   not null references reviewers(reviewer),
    review_date     date   not null,
    review_url      text   not null,
    book_isbn       text   not null,
    review          text   not null,
    rating          int    not null,
    constraint book_review_pkey primary key (review_author, book_title)
);

---------------------------------------------------------------------------
-- Details of each book present in the system
---------------------------------------------------------------------------
create table book_details(
    id              serial  not null,
    title           text    not null,
    author          text    not null,
    length          int     not null,
    publisher       text    not null,
    date_published  date    not null,
    isbn_10         text    not null,
    isbn_13         text    not null,
    page_url        text    not null,
    review_page_url text    not null,
);

---------------------------------------------------------------------------
-- count of the number of reviews made by each reviewer
---------------------------------------------------------------------------
create materialized view review_counts as
    select review_author, count (*) from reviews 
        group by review_author;


---------------------------------------------------------------------------
-- Table of filtered reviews.
---------------------------------------------------------------------------
create table author_review(
    id              serial  not null primary key,
    review_author   text    not null,
    review          text    not null,
    rating          int     not null
);

create table words(
    word        text    not null primary key,
    doc_count   int     not null
);

---------------------------------------------------------------------------
-- Processed Review Data
---------------------------------------------------------------------------


create table emotions(
    id      serial      not null,
    emotion text        not null primary key
);


create table emolex(
    id              serial      not null,
    word            text        not null
    anger           boolean     not null,
    anticipation    boolean     not null,
    disgust         boolean     not null,
    fear            boolean     not null,
    joy             boolean     not null,
    negative        boolean     not null,
    positive        boolean     not null,
    sadness         boolean     not null,
    surprise        boolean     not null,
    trust           boolean     not null    
);

---------------------------------------------------------------------------
-- Processed Review Data
---------------------------------------------------------------------------

create table review_emo_counts(
    id              serial      not null references author_review(id),
    emo_id          serial      not null,
    anger           int         not null,
    anticipation    int         not null,
    disgust         int         not null,
    fear            int         not null,
    joy             int         not null,
    negative        int         not null,
    positive        int         not null,
    sadness         int         not null,
    surprise        int         not null,
    trust           int         not null
);

create table review_data(
    id              serial      not null references author_review(id),
    word_count      int         not null,
    avg_word_length float       not null,
    sent_count      int         not null,
    avg_sent_length float       not null,
    unigram_counts  float       not null,
    bigram_counts   float       not null,
    trigram_counts  float       not null,
    emo_counts      serial      references review_emo_counts()
);

commit;