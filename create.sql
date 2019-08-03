CREATE TABLE newgram.users (
    id INT UNSIGNED UNIQUE AUTO_INCREMENT NOT NULL,

    username VARCHAR (32) UNIQUE NOT NULL,
    bio VARCHAR (256) NOT NULL DEFAULT "",
    email VARCHAR (128) UNIQUE NOT NULL,
--    verified TINYINT NOT NULL DEFAULT 0,
    password_hash VARCHAR (93) NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE newgram.uploads (
    id INT UNSIGNED UNIQUE AUTO_INCREMENT NOT NULL,

    description VARCHAR (128) NOT NULL DEFAULT "",
    upload_date INT UNSIGNED NOT NULL DEFAULT (UNIX_TIMESTAMP()),

    image MEDIUMBLOB NOT NULL,

    uploader INT UNSIGNED,

    CONSTRAINT uploader_cx
    FOREIGN KEY uploader_fk (uploader)
    REFERENCES users (id)
    ON DELETE SET NULL,

    PRIMARY KEY (id)
);

CREATE TABLE newgram.comments (
    id INT UNSIGNED UNIQUE AUTO_INCREMENT NOT NULL,

    content VARCHAR(160) NOT NULL,
    post INT UNSIGNED NOT NULL,
    commenter INT UNSIGNED,

    CONSTRAINT post_cx
    FOREIGN KEY post_fk (post)
    REFERENCES uploads (id)
    ON DELETE CASCADE,

    CONSTRAINT commenter_cx
    FOREIGN KEY commenter_fk (commenter)
    REFERENCES users (id)
    ON DELETE SET NULL,

    PRIMARY KEY (id)
);