CREATE TABLE newgram.users (
    id INT UNSIGNED UNIQUE AUTO_INCREMENT NOT NULL,

    username VARCHAR (32) UNIQUE NOT NULL,
    bio VARCHAR (256) NOT NULL DEFAULT "",
    email VARCHAR (128) NOT NULL,
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