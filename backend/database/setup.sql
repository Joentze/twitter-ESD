-- Create Twitter-like app database
-- Drop the database if it exists (for testing purposes)
DROP DATABASE IF EXISTS twitter_app;

-- Create a new database
CREATE DATABASE twitter_app;

-- Use the created database
USE twitter_app;

-- Create users table
CREATE TABLE users (
    uid INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Create tweets table
CREATE TABLE tweets (
    tweet_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Seed the database with fake data
-- Insert users
INSERT INTO
    users (username, email, password_hash)
VALUES
    (
        'user1',
        'user1@example.com',
        'hashed_password_1'
    ),
    (
        'user2',
        'user2@example.com',
        'hashed_password_2'
    ),
    (
        'user3',
        'user3@example.com',
        'hashed_password_3'
    );

-- Insert tweets
INSERT INTO
    tweets (user_id, content)
VALUES
    (1, 'This is a tweet from user1.'),
    (2, 'Tweeting like user2.'),
    (3, 'User3 joining the conversation.');

-- Add more data as needed
-- Display success message
SELECT
    'Database created and seeded successfully!' AS message;