CREATE TABLE IF NOT EXISTS accounts (
        "account_id" INTEGER PRIMARY KEY,
        "account_role" INTEGER NOT NULL,
        "account_username" VARCHAR(256) NOT NULL UNIQUE,
        "account_password_hash" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
        "post_id" INTEGER PRIMARY KEY,
        "post_creator_id" INTEGER NOT NULL,
        "attachments" TEXT NOT NULL,
        "tags" TEXT,
        "description" text,
        "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "updated_at" TIMESTAMP,
        FOREIGN KEY (post_creator_id) REFERENCES  accounts(account_id)
);

CREATE TABLE IF NOT EXISTS tags (
        "tag_id" INTEGER PRIMARY KEY,
        "tag_name" VARCHAR(256) NOT NULL
);
