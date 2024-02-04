-- Create Twitter-like app database
-- Drop the database if it exists (for testing purposes)
DROP DATABASE IF EXISTS twitter_app;

-- Create a new database
CREATE DATABASE twitter_app;

-- Use the created database
USE twitter_app;

-- Create users table
CREATE TABLE users (
    user_id CHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Create tweets table
CREATE TABLE tweets (
    tweet_id CHAR(36) PRIMARY KEY,
    user_id CHAR(36),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Seed the database with fake data
-- Insert users
INSERT INTO
    users (user_id, username, email, password_hash)
VALUES
    (
        '88cd187b-ce48-42d1-8696-2a8c756861b4',
        'user1',
        'user1@example.com',
        'hashed_password_1'
    ),
    (
        'beebba51-d600-4927-a908-a2af174982cd',
        'user2',
        'user2@example.com',
        'hashed_password_2'
    ),
    (
        '9d84387d-8f38-4b1b-b91a-e39e50cbd1c8',
        'user3',
        'user3@example.com',
        'hashed_password_3'
    );

-- Insert tweets
INSERT INTO
    tweets (tweet_id, user_id, content)
VALUES
    ('bdfd727d-6a9f-4229-9200-3324473eb805', '88cd187b-ce48-42d1-8696-2a8c756861b4', 'This is a tweet from user1.'),
    ('e19ec413-fe1d-43b8-a964-238f3cbce6cc', 'beebba51-d600-4927-a908-a2af174982cd', 'Tweeting like user2.'),
    ('2b235a33-dcb9-4d99-b5e3-7f0260083b92', '9d84387d-8f38-4b1b-b91a-e39e50cbd1c8', 'User3 joining the conversation.');

-- Add more data as needed
-- Display success message
SELECT
    'Database created and seeded successfully!' AS message;
