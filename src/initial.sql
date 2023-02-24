CREATE TABLE IF NOT EXISTS accounts (
        "account_id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "account_username" VARCHAR(512) NOT NULL UNIQUE,
        "account_password" TEXT NOT NULL,
        "account_role" INTEGER NOT NULL,
        "account_created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        "account_api_key" VARCHAR(64),
        "account_locked" BOOLEAN DEFAULT "FALSE"
);

CREATE TABLE IF NOT EXISTS posts (
        "post_id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "post_creator_id" INTEGER NOT NULL,
        "post_description" TEXT,
        "post_media_id" TEXT NOT NULL,
        "post_created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "post_updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_creator_id) REFERENCES  accounts(account_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tags (
        "tag_id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "tag_name" VARCHAR(256) NOT NULL,
        "tag_namespace" VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS tagsofposts (
        "post_id" INTEGER,
        "tag_id" INTEGER,
        PRIMARY KEY (post_id, tag_id),
        FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE,
        FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
);
