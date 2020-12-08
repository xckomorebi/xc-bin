CREATE TABLE follower(
    id INTEGER PRIMARY KEY NOT NULL,
    followers_id TEXT,
    new_followers_id TEXT,
    new_unfollowers_id TEXT,
    num_followers int
    update_at TIMESTAMP NOT NULL DEFAULT CURRENT_DATE
);


CREATE TABLE users(
    uid INTERGER NOT NULL,
    name VARCHAR(128),
    used_name TEXT,
    still_follower TINYINT
);