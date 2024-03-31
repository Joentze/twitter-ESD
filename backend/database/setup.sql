-- Create Twitter-like app database
-- Drop the database if it exists (for testing purposes)
DROP DATABASE IF EXISTS twitter_app;

-- Create a new database
CREATE DATABASE twitter_app;

-- Use the created database
USE twitter_app;

-- Create users table
CREATE TABLE USERS (
    uid VARCHAR(100) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    is_private BIT DEFAULT 0 NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE FOLLOWS (
    follower_id VARCHAR(100) NOT NULL,
    followed_id VARCHAR(100) NOT NULL,
    date_followed TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (follower_id, followed_id),
    FOREIGN KEY (follower_id) REFERENCES USERS(uid) ON DELETE cascade,
    FOREIGN KEY (followed_id) REFERENCES USERS(uid) ON DELETE cascade
);

CREATE TABLE POSTS(
    post_id CHAR(36) NOT NULL PRIMARY KEY,
    poster_uid VARCHAR(100) NOT NULL,
    post_content VARCHAR(300),
    post_location VARCHAR(300),
    post_images JSON,
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (poster_uid) REFERENCES USERS(uid) ON DELETE cascade
);

CREATE TABLE LIKES(
    uid VARCHAR(100) NOT NULL,
    post_id CHAR(36) NOT NULL,
    date_liked TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (uid, post_id),
    FOREIGN KEY (uid) REFERENCES USERS(uid) ON DELETE cascade,
    FOREIGN KEY (post_id) REFERENCES POSTS(post_id) ON DELETE cascade
);

CREATE TABLE COMMENTS(
    comment_id CHAR(36) NOT NULL,
    commenter_uid CHAR(100) NOT NULL,
    post_id CHAR(36) NOT NULL,
    content VARCHAR(300) NOT NULL,
    date_commented TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (comment_id, commenter_uid, post_id),
    FOREIGN KEY (commenter_uid) REFERENCES USERS(uid) ON DELETE cascade,
    FOREIGN KEY (post_id) REFERENCES POSTS(post_id) ON DELETE cascade
);

-- Seed USERS table with fake data
INSERT INTO
    USERS (uid, username, email, is_private, created_on)
VALUES
    (
        'user1_uid',
        'user1',
        'user1@example.com',
        0,
        '2024-02-08 12:00:00'
    ),
    (
        'user2_uid',
        'user2',
        'user2@example.com',
        0,
        '2024-02-08 12:00:00'
    ),
    (
        'user3_uid',
        'user3',
        'user3@example.com',
        1,
        '2024-02-08 12:00:00'
    ),
    (
        'user4_uid',
        'user4',
        'user4@example.com',
        0,
        '2024-02-08 12:00:00'
    );

-- Seed FOLLOWS table with fake data
INSERT INTO
    FOLLOWS (follower_id, followed_id, date_followed)
VALUES
    ('user1_uid', 'user2_uid', '2024-02-08 12:01:00'),
    ('user2_uid', 'user1_uid', '2024-02-08 12:02:00'),
    ('user1_uid', 'user3_uid', '2024-02-08 12:03:00'),
    ('user2_uid', 'user3_uid', '2024-02-08 12:04:00'),
    ('user3_uid', 'user1_uid', '2024-02-08 12:05:00');

-- Seed POSTS table with fake data
 INSERT INTO
     POSTS (
         post_id,
         poster_uid,
         post_content,
         post_location,
         post_images,
         date_posted
     )
 VALUES
     (
         'post1_id',
         'user1_uid',
         'Hello World!',
         'New York',
         '["image1.jpg", "image2.jpg"]',
         '2024-02-08 12:10:00'
     ),
     (
         'post2_id',
         'user2_uid',
         'Good morning!',
         'Los Angeles',
         '["image3.jpg"]',
         '2024-02-08 12:20:00'
     ),
     (
         'post3_id',
         'user3_uid',
         'Feeling happy today!',
         'Chicago',
         '[]',
         '2024-02-08 12:30:00'
     );
 
 -- Seed LIKES table with fake data
 INSERT INTO
     LIKES (uid, post_id, date_liked)
 VALUES
     ('user1_uid', 'post2_id', '2024-02-08 12:11:00'),
     ('user2_uid', 'post1_id', '2024-02-08 12:12:00'),
     ('user3_uid', 'post1_id', '2024-02-08 12:13:00'),
     ('user1_uid', 'post3_id', '2024-02-08 12:14:00'),
     ('user2_uid', 'post3_id', '2024-02-08 12:15:00');
 
 -- Seed COMMENTS table with fake data
 INSERT INTO
     COMMENTS (
         comment_id,
         commenter_uid,
         post_id,
         content,
         date_commented
     )
 VALUES
     (
         'comment1_id',
         'user1_uid',
         'post3_id',
         'Great!',
         '2024-02-08 12:31:00'
     ),
     (
         'comment2_id',
         'user2_uid',
         'post2_id',
         'Nice!',
         '2024-02-08 12:32:00'
     ),
     (
         'comment3_id',
         'user3_uid',
         'post1_id',
         'Awesome!',
         '2024-02-08 12:33:00'
     );
